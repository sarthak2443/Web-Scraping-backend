"""
Simple test to check if we can access Twitter/X and scrape basic content
"""
import asyncio
from playwright.async_api import async_playwright

async def test_twitter_access():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to False to see what happens
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("Navigating to Twitter...")
            await page.goto("https://twitter.com/search?q=%23nifty50&f=live", timeout=30000)
            await page.wait_for_load_state("domcontentloaded", timeout=15000)
            await asyncio.sleep(3)
            
            # Check what we can see
            title = await page.title()
            print(f"Page title: {title}")
            
            # Look for any articles
            articles = await page.query_selector_all("article")
            print(f"Found {len(articles)} article elements")
            
            # Check for login requirements or blocking
            login_elements = await page.query_selector_all("text=Log in")
            print(f"Found {len(login_elements)} login prompts")
            
            # Take a screenshot for debugging
            await page.screenshot(path="twitter_test.png")
            print("Screenshot saved as twitter_test.png")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_twitter_access())
