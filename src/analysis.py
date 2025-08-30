"""
Text-to-signal conversion:
 - Use TF-IDF to vectorize tweet content
 - Dimensionality reduction with TruncatedSVD
 - Generate composite trading signal with confidence
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np


def compute_tfidf_signals(df, n_components=50):
    """Compute TF-IDF signals from tweet DataFrame."""
    # Handle empty DataFrame
    if len(df) == 0 or "content" not in df.columns:
        return pd.DataFrame({
            "tweet_url": [],
            "timestamp": [],
            "signal_score": [],
            "signal_confidence": []
        })
    
    texts = df["content"].fillna("")

    vect = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vect.fit_transform(texts)

    # reduce dimensionality
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    Xr = svd.fit_transform(X)

    # composite score: use first component as heuristic
    comp_score = Xr[:, 0]

    # normalize
    scores = (comp_score - np.nanmean(comp_score)) / (np.nanstd(comp_score) + 1e-9)

    df_signals = pd.DataFrame(
        {
            "tweet_url": df.get("tweet_url"),
            "timestamp": df["timestamp"],
            "signal_score": scores,
            "signal_confidence": np.abs(scores),  # absolute value as proxy confidence
        }
    )
    return df_signals


if __name__ == "__main__":
    df = pd.read_parquet("data/tweets.parquet")
    signals = compute_tfidf_signals(df)
    signals.to_parquet("data/signals.parquet")
    print("Wrote data/signals.parquet")
