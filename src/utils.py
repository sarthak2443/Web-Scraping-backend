import logging
import random
from datetime import datetime, timezone, timedelta

LOG_FORMAT = "%(asctime)s — %(levelname)s — %(message)s"

def configure_logging(level=logging.INFO):
    logging.basicConfig(level=level, format=LOG_FORMAT)

async def jitter_sleep(min_secs=0.5, max_secs=2.5):
    import asyncio
    await asyncio.sleep(random.uniform(min_secs, max_secs))

def utc_now():
    return datetime.now(timezone.utc)

def since_24_hours_iso():
    return (utc_now() - timedelta(hours=24)).isoformat()

def safe_get(d, k, default=None):
    return d.get(k, default)
