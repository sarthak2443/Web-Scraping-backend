"""
Asynchronous Playwright-based scraper for X/Twitter hashtags.

Features:
 - Scrape tweets for given hashtags
 - Extract username, content, timestamp, metrics, mentions, hashtags, url
 - Handle timeouts and login walls more gracefully
 - Configurable headless mode for debugging
"""

from playwright.async_api import async_playwright
import asyncio
from datetime import datetime, timedelta
import re
from .utils import jitter_sleep, utc_now

HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]


async def extract_tweet_from_article(article_el):
    """Extract fields from a single tweet <article> element."""
    try:
        # username
        user_el = await article_el.query_selector('div[dir="ltr"] span')
        username = (await user_el.inner_text()) if user_el else ""

        # content
        content_el = await article_el.query_selector('div[lang]')
        content = (await content_el.inner_text()) if content_el else ""

        # timestamp
        time_el = await article_el.query_selector("time")
        timestamp_iso = None
        if time_el:
            ts = await time_el.get_attribute("datetime")
            timestamp_iso = ts

        # metrics: likes, retweets, replies
        metrics = {}
        metric_els = await article_el.query_selector_all(
            'div[data-testid="like"], div[data-testid="retweet"], div[data-testid="reply"]'
        )
        for met in metric_els:
            try:
                lbl = await met.get_attribute("aria-label")
                m = re.match(r"([0-9,\.]+)\s+([A-Za-z]+)", lbl or "")
                if m:
                    val = int(m.group(1).replace(",", "").split(".")[0])
                    key = m.group(2).lower()
                    metrics[key] = val
            except Exception:
                continue

        # mentions & hashtags
        mentions = re.findall(r"@\w+", content)
        hashtags = re.findall(r"#\w+", content)

        # tweet url
        url_el = await article_el.query_selector('a[href*="/status/"]')
        tweet_url = None
        if url_el:
            href = await url_el.get_attribute("href")
            if href:
                tweet_url = (
                    "https://twitter.com" + href if href.startswith("/") else href
                )

        return {
            "username": username,
            "timestamp": timestamp_iso,
            "content": content,
            "metrics": metrics,
            "mentions": mentions,
            "hashtags": hashtags,
            "tweet_url": tweet_url,
        }
    except Exception:
        return None


async def scrape_hashtag(page, hashtag, max_tweets=500, since_dt=None):
    """Scrape tweets for a single hashtag until max_tweets or older than since_dt."""
    results = []
    seen_tweets = set()  # Track unique tweets to avoid duplicates
    q = f"%23{hashtag} lang:en OR lang:hi"
    url = f"https://twitter.com/search?q={q}&f=live"

    # Load page with reduced timeout
    await page.goto(url, timeout=30_000)
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass  # continue even if timeout
    await asyncio.sleep(2)  # reduced initial wait

    scroll_tries = 0
    no_new_tweets_count = 0
    while len(results) < max_tweets and scroll_tries < 50:  # Reduced from 500 to 50
        articles = await page.query_selector_all("article")
        initial_count = len(results)
        
        for art in articles:
            data = await extract_tweet_from_article(art)
            if not data or not data.get("content"):
                continue
                
            # Skip duplicates
            tweet_id = data.get("content", "")[:100]  # Use first 100 chars as unique identifier
            if tweet_id in seen_tweets:
                continue
            seen_tweets.add(tweet_id)
                
            ts = data.get("timestamp")
            if ts and since_dt:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    dt = None
                if dt and dt < since_dt:
                    return results
            results.append(data)
            
            if len(results) >= max_tweets:
                break
        
        # Check if we found new tweets this scroll
        if len(results) == initial_count:
            no_new_tweets_count += 1
            if no_new_tweets_count >= 3:  # Stop if no new tweets for 3 scrolls
                break
        else:
            no_new_tweets_count = 0
            
        # scroll with reduced delay
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await jitter_sleep(0.2, 0.5)  # Reduced from 0.5-1.5 to 0.2-0.5
        scroll_tries += 1

    return results


async def run_scraper(hashtags=HASHTAGS, target_per_hashtag=500, headless=True, proxy=None):
    """Run scraper for all hashtags and return collected tweet dicts."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, proxy=proxy)
        context = await browser.new_context()
        page = await context.new_page()
        since_dt = utc_now() - timedelta(hours=24)

        collected = []
        for tag in hashtags:
            chunk = await scrape_hashtag(
                page, tag, max_tweets=target_per_hashtag, since_dt=since_dt
            )
            collected.extend(chunk)
            await jitter_sleep(1, 2.5)

        await browser.close()
        return collected


if __name__ == "__main__":
    async def _main():
        # Debug run (headless=False so you can see the browser)
        items = await run_scraper(target_per_hashtag=50, headless=False)
        print(f"Collected {len(items)} tweets")

    asyncio.run(_main())
