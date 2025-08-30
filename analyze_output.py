"""
Sample output analysis script.
Demonstrates how to work with the generated data files.
"""

import pandas as pd
from pathlib import Path
import numpy as np

def analyze_tweets_data():
    """Analyze the tweets.parquet file and display key insights."""
    
    tweets_path = Path("data/tweets.parquet")
    if not tweets_path.exists():
        print("❌ tweets.parquet not found. Please run the pipeline first.")
        return
    
    print("📊 Loading and analyzing tweets data...")
    df = pd.read_parquet(tweets_path)
    
    print(f"\n🔍 Dataset Overview:")
    print(f"   • Total tweets: {len(df):,}")
    print(f"   • Unique users: {df['username'].nunique():,}")
    print(f"   • Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"   • Columns: {list(df.columns)}")
    
    print(f"\n📈 Content Analysis:")
    print(f"   • Average content length: {df['content'].str.len().mean():.1f} characters")
    print(f"   • Tweets with hashtags: {df['hashtags'].apply(len).sum():,}")
    print(f"   • Tweets with mentions: {df['mentions'].apply(len).sum():,}")
    
    # Most active users
    print(f"\n👤 Top 5 Most Active Users:")
    top_users = df['username'].value_counts().head()
    for user, count in top_users.items():
        print(f"   • @{user}: {count} tweets")
    
    # Most common hashtags
    print(f"\n🏷️ Most Common Hashtags:")
    all_hashtags = []
    for hashtag_list in df['hashtags']:
        all_hashtags.extend(hashtag_list)
    
    hashtag_counts = pd.Series(all_hashtags).value_counts().head()
    for tag, count in hashtag_counts.items():
        print(f"   • {tag}: {count} occurrences")
    
    # Sample tweets
    print(f"\n📝 Sample Tweets:")
    for i, row in df.head(3).iterrows():
        print(f"   • @{row['username']}: {row['content'][:100]}...")
    
    return df

def analyze_signals_data():
    """Analyze the signals.parquet file and display trading insights."""
    
    signals_path = Path("data/signals.parquet")
    if not signals_path.exists():
        print("❌ signals.parquet not found. Please run the pipeline first.")
        return
    
    print("\n🎯 Loading and analyzing signals data...")
    df = pd.read_parquet(signals_path)
    
    print(f"\n🔍 Signals Overview:")
    print(f"   • Total signals: {len(df):,}")
    print(f"   • Signal range: {df['signal_score'].min():.3f} to {df['signal_score'].max():.3f}")
    print(f"   • Average confidence: {df['signal_confidence'].mean():.3f}")
    print(f"   • High confidence signals (>0.5): {(df['signal_confidence'] > 0.5).sum():,}")
    
    # Signal distribution
    bullish = (df['signal_score'] > 0).sum()
    bearish = (df['signal_score'] < 0).sum()
    neutral = (df['signal_score'] == 0).sum()
    
    print(f"\n📊 Signal Distribution:")
    print(f"   • Bullish signals: {bullish:,} ({bullish/len(df)*100:.1f}%)")
    print(f"   • Bearish signals: {bearish:,} ({bearish/len(df)*100:.1f}%)")
    print(f"   • Neutral signals: {neutral:,} ({neutral/len(df)*100:.1f}%)")
    
    # Top signals
    print(f"\n⬆️ Top 5 Bullish Signals:")
    top_bullish = df.nlargest(5, 'signal_score')
    for _, row in top_bullish.iterrows():
        print(f"   • Score: {row['signal_score']:.3f}, Confidence: {row['signal_confidence']:.3f}")
    
    print(f"\n⬇️ Top 5 Bearish Signals:")
    top_bearish = df.nsmallest(5, 'signal_score')
    for _, row in top_bearish.iterrows():
        print(f"   • Score: {row['signal_score']:.3f}, Confidence: {row['signal_confidence']:.3f}")
    
    return df

def create_visualizations():
    """Create sample visualizations of the data."""
    
    print("\n📊 Visualization Analysis (Text-based):")
    try:
        # Load data
        tweets_df = pd.read_parquet("data/tweets.parquet")
        signals_df = pd.read_parquet("data/signals.parquet")
        
        # Signal score histogram (text-based)
        print("\n📈 Signal Score Distribution (histogram):")
        score_bins = pd.cut(signals_df['signal_score'], bins=10)
        score_hist = score_bins.value_counts().sort_index()
        for interval, count in score_hist.items():
            bar = "█" * max(1, int(count * 50 / score_hist.max()))
            print(f"   {interval}: {bar} ({count})")
        
        # Tweet length analysis
        print("\n📝 Tweet Length Statistics:")
        tweet_lengths = tweets_df['content'].str.len()
        print(f"   • Min: {tweet_lengths.min()} chars")
        print(f"   • Max: {tweet_lengths.max()} chars")
        print(f"   • Mean: {tweet_lengths.mean():.1f} chars")
        print(f"   • Median: {tweet_lengths.median():.1f} chars")
        
    except Exception as e:
        print(f"   Error in visualization: {e}")

def main():
    """Main analysis function."""
    print("🚀 Stock Market Sentiment Analysis - Sample Output Analysis")
    print("=" * 60)
    
    # Analyze tweets
    tweets_df = analyze_tweets_data()
    
    # Analyze signals
    signals_df = analyze_signals_data()
    
    # Create visualizations
    create_visualizations()
    
    print("\n" + "=" * 60)
    print("✅ Analysis complete! Check the generated files:")
    print("   • data/tweets.parquet - Processed tweet data")
    print("   • data/signals.parquet - Trading signals")
    print("\n💡 Next steps:")
    print("   • Backtest signals against historical market data")
    print("   • Implement real-time monitoring dashboard")
    print("   • Add more sophisticated NLP models")
    print("\n📊 For visualizations, install matplotlib:")
    print("   pip install matplotlib seaborn")

if __name__ == "__main__":
    main()
