"""
Cleaning pipeline:
 - Normalize whitespace
 - Remove invisible/control characters
 - Handle unicode
 - Deduplicate by tweet_url or content hash
"""
import re
import pandas as pd
import hashlib
from dateutil import parser

RE_WS = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Normalize whitespace and strip text."""
    if not isinstance(text, str):
        return ""
    t = text.strip()
    t = RE_WS.sub(" ", t)
    return t


def compute_hash(row):
    """Compute hash from tweet_url + content to deduplicate."""
    key = (row.get("tweet_url") or "") + "||" + (row.get("content") or "")
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def to_dataframe(records):
    """Convert list of dicts -> pandas DataFrame with cleaning + deduplication."""
    df = pd.DataFrame(records)

    if "content" in df:
        df["content"] = df["content"].apply(normalize_text)
    if "username" in df:
        df["username"] = df["username"].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # parse timestamp safely
    def parse_ts(x):
        try:
            return parser.isoparse(x)
        except Exception:
            return pd.NaT

    if "timestamp" in df:
        df["timestamp"] = df["timestamp"].apply(parse_ts)

    # compute hash for dedupe
    df["hash"] = df.apply(compute_hash, axis=1)

    # drop duplicates
    df = df.drop_duplicates(subset=["hash"])

    return df
