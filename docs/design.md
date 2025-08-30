# Technical Design Document
## Stock Market Sentiment Analysis Pipeline

### Executive Summary

This document outlines the technical architecture and design decisions for a comprehensive social media sentiment analysis pipeline targeting Indian stock markets. The system implements modern software engineering practices with a focus on scalability, maintainability, and robust error handling.

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Source   │    │   Processing    │    │     Storage     │
│   (X/Twitter)   │───▶│     Pipeline    │───▶│   (Parquet)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   ML Analysis   │
                       │   (TF-IDF)      │
                       └─────────────────┘
```

### Core Components

#### 1. Data Acquisition Layer (`scraper.py`)

**Technology Stack:**
- **Playwright**: Asynchronous browser automation
- **Chromium Engine**: Headless browser for web scraping
- **AsyncIO**: Concurrent processing for performance

**Design Decisions:**
- **Asynchronous Architecture**: Enables concurrent processing of multiple hashtags
- **Graceful Degradation**: Handles rate limiting and access restrictions
- **Configurable Timeouts**: Balanced between reliability and performance
- **Smart Scrolling**: Early termination when no new content is found

**Key Features:**
```python
async def scrape_hashtag(page, hashtag, max_tweets=500):
    # Duplicate detection using content hashing
    # Progressive timeout handling
    # Structured data extraction
```

#### 2. Data Processing Layer (`cleaner.py`)

**Processing Pipeline:**
1. **Text Normalization**: Whitespace standardization and Unicode handling
2. **Data Validation**: Type checking and null value handling
3. **Deduplication**: SHA-256 hashing for content uniqueness
4. **Timestamp Parsing**: ISO format standardization with error handling

**Deduplication Strategy:**
```python
def compute_hash(row):
    key = (row.get("tweet_url") or "") + "||" + (row.get("content") or "")
    return hashlib.sha256(key.encode("utf-8")).hexdigest()
```

#### 3. Storage Layer (`storage.py`)

**Technology Choice: Apache Parquet**

**Advantages:**
- **Columnar Storage**: 50-80% size reduction compared to CSV
- **Schema Evolution**: Supports adding new fields without breaking existing data
- **Fast Analytics**: Optimized for analytical queries
- **Cross-Platform**: Compatible with Pandas, Spark, and cloud platforms

**Implementation:**
- **Append Mode**: Incremental data loading without full rewrites
- **Compression**: Built-in compression for storage efficiency
- **Type Preservation**: Maintains data types across read/write cycles

#### 4. Machine Learning Pipeline (`analysis.py`)

**TF-IDF Signal Generation:**

```python
def compute_tfidf_signals(df, n_components=50):
    # 1. Text Vectorization (5000 features, 1-2 grams)
    vect = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    
    # 2. Dimensionality Reduction (50 components)
    svd = TruncatedSVD(n_components=50, random_state=42)
    
    # 3. Signal Extraction (first principal component)
    # 4. Z-score Normalization
```

**Signal Interpretation:**
- **Positive Values**: Bullish sentiment indicators
- **Negative Values**: Bearish sentiment indicators
- **Magnitude**: Signal strength and confidence level

#### 5. Orchestration Layer (`orchestrator.py`)

**Pipeline Coordination:**
1. **Data Acquisition**: Scraping with fallback to mock data
2. **Data Processing**: Cleaning and deduplication
3. **Storage Operations**: Parquet file management
4. **Analysis Execution**: Signal generation and storage

**Error Handling Strategy:**
- **Graceful Fallbacks**: Mock data when scraping fails
- **Comprehensive Logging**: Structured logging for debugging
- **Exception Isolation**: Prevents single component failure from breaking the pipeline

### Performance Optimizations

#### Scraping Performance
- **Reduced Scroll Attempts**: 500 → 50 maximum scrolls
- **Optimized Timeouts**: 120s → 30s page load timeout
- **Efficient Delays**: 0.5-1.5s → 0.2-0.5s between operations
- **Early Termination**: Stop when no new content found

#### Memory Management
- **Streaming Processing**: Process data in chunks to minimize memory usage
- **Efficient Data Structures**: Use pandas for optimized operations
- **Garbage Collection**: Explicit cleanup of browser resources

#### Storage Optimization
- **Columnar Format**: Parquet for analytical workloads
- **Compression**: Built-in compression algorithms
- **Incremental Updates**: Append-only operations

### Data Flow Architecture

```
Raw Tweets → Text Cleaning → Deduplication → Parquet Storage
                                               ↓
Signal Storage ← ML Processing ← Feature Extraction
```

### Error Handling and Resilience

#### Multi-Level Error Handling
1. **Network Level**: Timeout and retry mechanisms
2. **Data Level**: Validation and type checking
3. **Processing Level**: Exception isolation and logging
4. **System Level**: Graceful degradation and fallbacks

#### Fallback Mechanisms
- **Mock Data Generator**: Realistic test data when scraping fails
- **Empty Dataset Handling**: Graceful processing of zero records
- **Partial Failure Recovery**: Continue processing with available data

### Monitoring and Observability

#### Logging Strategy
```python
configure_logging()
logger = logging.getLogger(__name__)

# Structured logging with context
logger.info(f'Collected {len(records)} raw records')
logger.warning('No records from scraper, using mock data')
logger.error(f'Scraper failed: {e}')
```

#### Metrics Collection
- **Data Volume**: Records processed per run
- **Processing Time**: Pipeline execution duration
- **Error Rates**: Failed operations tracking
- **Data Quality**: Deduplication ratios and cleaning statistics

### Security Considerations

#### Data Privacy
- **No Personal Data Storage**: Only public tweet content
- **URL Sanitization**: Clean external references
- **Anonymization**: No user tracking or profiling

#### Access Control
- **Rate Limiting Compliance**: Respect platform limits
- **User-Agent Rotation**: Avoid detection mechanisms
- **Ethical Scraping**: Follow robots.txt and terms of service

### Scalability Design

#### Horizontal Scaling Opportunities
1. **Multi-Platform Support**: Extend to Reddit, Discord, news sources
2. **Distributed Processing**: Implement with Celery or Ray
3. **Cloud Deployment**: Containerization with Docker/Kubernetes
4. **Stream Processing**: Real-time data ingestion with Apache Kafka

#### Vertical Scaling Options
1. **Parallel Hashtag Processing**: Concurrent scraping tasks
2. **Batch Processing**: Process multiple time windows simultaneously
3. **Memory Optimization**: Streaming data processing
4. **CPU Optimization**: Vectorized operations for ML processing

### Testing Strategy

#### Unit Testing
- **Component Isolation**: Test each module independently
- **Mock Data Testing**: Validate pipeline with synthetic data
- **Edge Case Handling**: Test error conditions and boundary cases

#### Integration Testing
- **End-to-End Validation**: Complete pipeline testing
- **Data Quality Checks**: Validate output data integrity
- **Performance Testing**: Benchmark processing times

### Future Architecture Enhancements

#### Real-Time Processing
```
Kafka/Redis → Stream Processor → Real-time Signals → WebSocket API
```

#### Advanced ML Pipeline
```
Raw Text → Preprocessing → BERT Embeddings → Ensemble Models → Signals
```

#### Microservices Architecture
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Scraper   │  │   Cleaner   │  │   Storage   │  │  Analysis   │
│   Service   │  │   Service   │  │   Service   │  │   Service   │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

### Conclusion

This architecture provides a robust, scalable foundation for social media sentiment analysis with clear separation of concerns, comprehensive error handling, and modern software engineering practices. The design prioritizes maintainability and extensibility while delivering immediate value through the core data pipeline.
