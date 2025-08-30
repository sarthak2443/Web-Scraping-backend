"""
Top-level orchestration script.
- Calls scraper to fetch raw records
- Cleans and deduplicates
- Stores to Parquet (append mode)
- Runs analysis to emit signals
"""

import asyncio
from .scraper import run_scraper
from .mock_data import generate_mock_tweets
from .cleaner import to_dataframe
from .storage import append_parquet, write_parquet
from .analysis import compute_tfidf_signals
from .utils import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)

async def main_async():
    logger.info('Starting scraper...')

    # Try to scrape real data, fallback to mock data if needed
    try:
        records = await run_scraper(target_per_hashtag=25, headless=True)
        logger.info(f'Collected {len(records)} raw records from scraper')
        
        if len(records) == 0:
            logger.warning('No records from scraper, using mock data for testing')
            records = generate_mock_tweets(100)
            logger.info(f'Generated {len(records)} mock records')
    except Exception as e:
        logger.error(f'Scraper failed: {e}. Using mock data for testing')
        records = generate_mock_tweets(100)
        logger.info(f'Generated {len(records)} mock records')

    df = to_dataframe(records)
    logger.info(f'After cleaning & dedupe: {len(df)} records')

    append_parquet(df, path='data/tweets.parquet')
    logger.info('Wrote data/tweets.parquet')

    signals = compute_tfidf_signals(df)
    write_parquet(signals, path='data/signals.parquet')
    logger.info('Wrote data/signals.parquet')

if __name__ == '__main__':
    asyncio.run(main_async())
