import pandas as pd
import os

# Paths
tweets_path = "data/tweets.parquet"
signals_path = "data/signals.parquet"

# Check if files exist
if not os.path.exists(tweets_path):
    print("❌ tweets.parquet not found. Run the scraper first.")
else:
    tweets = pd.read_parquet(tweets_path)
    print("\n✅ Tweets loaded:", len(tweets))
    print(tweets.head())

    # Export to CSV
    tweets.to_csv("tweets.csv", index=False)
    print("📄 Exported tweets.csv")

if not os.path.exists(signals_path):
    print("\n❌ signals.parquet not found. Run the scraper + analysis first.")
else:
    signals = pd.read_parquet(signals_path)
    print("\n✅ Signals loaded:", len(signals))
    print(signals.head())

    # Export to CSV
    signals.to_csv("signals.csv", index=False)
    print("📄 Exported signals.csv")
