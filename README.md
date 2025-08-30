# Stock Market Sentiment Analysis Pipeline

A comprehensive data pipeline that scrapes social media sentiment from X/Twitter for Indian stock market analysis, processes the data, and generates trading signals using machine learning techniques.

## 🎯 Project Overview

This project implements an end-to-end pipeline for collecting and analyzing social media sentiment related to Indian stock markets. It scrapes tweets for specific hashtags, performs data cleaning and deduplication, stores data efficiently, and generates trading signals using TF-IDF analysis.

### Key Features
- **Asynchronous Web Scraping**: High-performance scraping using Playwright
- **Data Processing**: Robust cleaning, normalization, and deduplication
- **Efficient Storage**: Parquet format for optimal data storage and retrieval
- **ML-based Signals**: TF-IDF vectorization with dimensionality reduction
- **Graceful Fallback**: Mock data generation when scraping is restricted
- **Professional Architecture**: Modular, maintainable, and well-documented code

## 🏗️ Project Structure

```
stock/
├── src/                    # Source code modules
│   ├── __init__.py        # Package initialization
│   ├── orchestrator.py    # Main pipeline orchestrator
│   ├── scraper.py         # Asynchronous Twitter/X scraper
│   ├── cleaner.py         # Data cleaning and normalization
│   ├── storage.py         # Parquet data storage utilities
│   ├── analysis.py        # TF-IDF signal generation
│   ├── mock_data.py       # Mock data generator for testing
│   └── utils.py           # Logging and utility functions
├── data/                  # Data storage directory
│   ├── tweets.parquet     # Processed tweet data
│   └── signals.parquet    # Generated trading signals
├── docs/                  # Documentation
│   └── design.md          # Technical design document
├── requirements.txt       # Python dependencies
├── run.sh                # Quick start script (Unix)
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock
   ```

2. **Set up virtual environment**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Unix/Linux/MacOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Run the pipeline**
   ```bash
   python -m src.orchestrator
   ```

## 📊 Sample Output

After running the pipeline, you'll find:

- `data/tweets.parquet`: Cleaned tweet data with metadata
- `data/signals.parquet`: Trading signals with confidence scores

### Sample Data Structure

**Tweets Data:**
| Field | Type | Description |
|-------|------|-------------|
| username | string | Twitter username |
| timestamp | datetime | Tweet timestamp |
| content | string | Tweet text content |
| metrics | object | Likes, retweets, replies |
| hashtags | array | Extracted hashtags |
| mentions | array | User mentions |
| tweet_url | string | Original tweet URL |

**Signals Data:**
| Field | Type | Description |
|-------|------|-------------|
| tweet_url | string | Reference to original tweet |
| timestamp | datetime | Signal timestamp |
| signal_score | float | TF-IDF based signal (-∞ to +∞) |
| signal_confidence | float | Confidence level (0 to 1) |

## 🔧 Configuration

### Target Hashtags
The scraper monitors these Indian stock market hashtags:
- `#nifty50` - Nifty 50 index discussions
- `#sensex` - BSE Sensex related tweets
- `#intraday` - Day trading conversations
- `#banknifty` - Bank Nifty index tweets

### Performance Tuning
Modify `src/orchestrator.py` to adjust:
```python
# Reduce for faster testing, increase for more data
target_per_hashtag=25  # tweets per hashtag
```

### Scraping Parameters
In `src/scraper.py`:
```python
max_tweets=500        # Maximum tweets per hashtag
since_dt=24_hours     # Time window for scraping
headless=True         # Browser visibility
```

## 🧪 Testing

The pipeline includes comprehensive error handling and fallback mechanisms:

1. **Mock Data Testing**: When X/Twitter blocks access, the system automatically generates realistic mock data
2. **Empty Data Handling**: Graceful handling of empty datasets
3. **Error Recovery**: Robust exception handling throughout the pipeline

Run with debug mode:
```bash
# See browser during scraping (for debugging)
python test_scraper.py
```

## 📈 Machine Learning Pipeline

### TF-IDF Signal Generation
1. **Text Vectorization**: Convert tweets to TF-IDF vectors (max 5000 features)
2. **Dimensionality Reduction**: TruncatedSVD to 50 components
3. **Signal Extraction**: First principal component as trading signal
4. **Normalization**: Z-score normalization for consistent scaling
5. **Confidence Scoring**: Absolute signal value as confidence metric

### Signal Interpretation
- **Positive signals**: Bullish sentiment detected
- **Negative signals**: Bearish sentiment detected
- **Confidence levels**: Higher absolute values indicate stronger signals

## 🛠️ Development

### Code Quality
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Detailed docstrings for all functions
- **Error Handling**: Robust exception management
- **Logging**: Structured logging throughout the pipeline
- **Modular Design**: Separation of concerns across modules

### Adding New Features
1. **New Data Sources**: Extend `scraper.py` with additional platforms
2. **Enhanced Signals**: Modify `analysis.py` for new ML models
3. **Custom Storage**: Update `storage.py` for different formats
4. **Additional Cleaning**: Enhance `cleaner.py` with new rules

## 🚨 Known Limitations

1. **Platform Restrictions**: X/Twitter may require authentication for access
2. **Rate Limiting**: Social media platforms enforce request limits
3. **Data Quality**: Social media data can be noisy and require careful preprocessing
4. **Market Hours**: Consider filtering signals by market trading hours

## 🔮 Future Enhancements

- [ ] Real-time streaming data ingestion
- [ ] Advanced NLP models (BERT, sentiment analysis)
- [ ] Multi-platform data collection (Reddit, Discord)
- [ ] Backtesting framework for signal validation
- [ ] Web dashboard for real-time monitoring
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team.

---

**Built with ❤️ for the Indian stock market community**
