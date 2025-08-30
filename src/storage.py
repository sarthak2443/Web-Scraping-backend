"""
Storage utilities:
 - Write DataFrame to Parquet
 - Append-friendly function for Parquet
"""
import pyarrow as pa
import pyarrow.parquet as pq
import os
import pandas as pd

DEFAULT_PATH = "data/tweets.parquet"


def write_parquet(df, path=DEFAULT_PATH, partition_cols=None):
    """Write DataFrame to a Parquet file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)


def append_parquet(df, path=DEFAULT_PATH):
    """Append DataFrame to an existing Parquet file (simple concat)."""
    if os.path.exists(path):
        existing = pd.read_parquet(path)
        merged = pd.concat([existing, df], ignore_index=True)
        write_parquet(merged, path)
    else:
        write_parquet(df, path)
