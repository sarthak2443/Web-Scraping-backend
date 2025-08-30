"""
Mock data generator for testing the pipeline when Twitter/X is not accessible
"""
import random
from datetime import datetime, timedelta

# Stock-related tweets content for realistic testing
MOCK_TWEETS = [
    "Nifty50 showing strong bullish momentum! Target 25000 #nifty50 #stockmarket",
    "Bank Nifty breaking resistance at 52000. Good time to enter long positions #banknifty",
    "Sensex rallying hard today! Blue chip stocks on fire #sensex #investing",
    "Intraday traders making good profits on IT stocks today #intraday #daytrading",
    "TCS and Infosys leading the charge in tech sector #nifty50 #techstocks",
    "Market sentiment very positive. FIIs buying heavily #stockmarket #investing",
    "Reliance showing weakness below 2800. Watch for breakdown #ril #sensex",
    "Banking stocks outperforming today. HDFC Bank up 3% #banknifty #banking",
    "Volatile session ahead. Trade with proper risk management #intraday #trading",
    "Auto sector stocks gaining momentum. Tata Motors up 5% #sensex #auto",
    "Small cap stocks rallying. Good time for stock picking #investing #smallcaps",
    "Pharma stocks under pressure. Dr Reddy down 2% #pharma #nifty50",
    "Energy stocks surging on crude oil rally #energy #sensex",
    "FMCG stocks defensive play in uncertain times #fmcg #investing",
    "Metal stocks volatile on global cues #metals #intraday"
]

USERNAMES = [
    "trader_pro", "stock_guru", "market_wizard", "invest_smart", "day_trader",
    "equity_expert", "nifty_tracker", "sensex_watch", "option_master", "swing_trader"
]

def generate_mock_tweets(count=100):
    """Generate mock tweet data for testing"""
    tweets = []
    base_time = datetime.utcnow()
    
    for i in range(count):
        content = random.choice(MOCK_TWEETS)
        username = random.choice(USERNAMES)
        
        # Add some variation to content
        if random.random() > 0.7:
            content += f" Target: {random.randint(24000, 26000)}"
        if random.random() > 0.8:
            content += f" @{random.choice(USERNAMES)}"
            
        tweet = {
            "username": username,
            "timestamp": (base_time - timedelta(hours=random.randint(0, 24))).isoformat() + "Z",
            "content": content,
            "metrics": {
                "likes": random.randint(0, 500),
                "retweets": random.randint(0, 100),
                "replies": random.randint(0, 50)
            },
            "mentions": [f"@{random.choice(USERNAMES)}" for _ in range(random.randint(0, 2))],
            "hashtags": [f"#{tag}" for tag in random.sample(["nifty50", "sensex", "intraday", "banknifty", "stockmarket", "investing"], random.randint(1, 3))],
            "tweet_url": f"https://twitter.com/{username}/status/{random.randint(1000000000000000000, 9999999999999999999)}"
        }
        tweets.append(tweet)
    
    return tweets
