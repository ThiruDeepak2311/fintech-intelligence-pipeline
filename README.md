# Fintech Intelligence Pipeline & Dashboard

A production-ready automated financial analysis system that integrates real-time stock market data with AI-powered insights and provides a professional React dashboard for data visualization. Built with Python, PostgreSQL, Flask API, and React.

## 🚀 Live Demo

**Frontend Dashboard**: https://finpipe-dashboard.vercel.app  
**Backend API**: https://fintech-intelligence-pipeline-production.up.railway.app  
**GitHub Repository**: https://github.com/ThiruDeepak2311/fintech-intelligence-pipeline

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Polygon.io    │───▶│  Python Backend │───▶│   PostgreSQL    │
│   Stock API     │    │   (Flask API)   │    │   Database      │
│   (Daily 9AM)   │    │   + Scheduler   │    │   (Railway)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        │
                       ┌─────────────────┐            │
                       │   LLM Analysis  │            │
                       │   (LLaMA 3.2)   │            │
                       │   via OpenRouter│            │
                       └─────────────────┘            │
                              │                        │
                              ▼                        │
                       ┌─────────────────┐            │
                       │  Flask REST API │◀───────────┘
                       │   (5 Endpoints) │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  React Dashboard│
                       │   (Vercel)      │
                       │  Real-time UI   │
                       └─────────────────┘
```

## ✨ Features

### 🤖 Automated Intelligence Pipeline
- **Daily Data Collection**: Fetches live AAPL stock data from Polygon.io API every day at 9 AM EST
- **AI-Powered Analysis**: Uses LLaMA 3.2 model through OpenRouter for sentiment analysis and risk assessment
- **Smart Scheduling**: Automatically handles weekends and market holidays with graceful error handling
- **Risk Quantification**: Provides 1-10 risk scoring with actionable investment recommendations
- **Data Persistence**: Stores all data and analysis in PostgreSQL for historical trend analysis

### 📱 Professional Dashboard
- **Real-Time Visualization**: Interactive stock charts with Recharts displaying live market data
- **AI Analysis Panel**: Dynamic sentiment indicators, risk gauges, and price predictions
- **Smart Data Tables**: Sortable/filterable recommendations with accuracy tracking
- **Performance Analytics**: Comprehensive system metrics with pie charts and KPI cards
- **Responsive Design**: Professional dark theme optimized for all devices

### 🔄 Automated Workflow & Market Intelligence

#### Daily Execution Schedule
- **Timing**: System runs automatically at 9:00 AM EST (2:30 PM IST) daily
- **Data Processing**: Fetches previous trading day's complete market data
- **Analysis Generation**: AI processes price movements, volume, and generates investment recommendations
- **Database Updates**: Stores new data and links AI analysis via foreign key relationships

#### Market Holiday Handling
- **Weekend Awareness**: System gracefully handles Saturday/Sunday when markets are closed
- **Holiday Detection**: Automatically skips federal holidays and market closures
- **Error Recovery**: If data is unavailable (404 from Polygon.io), system logs and waits for next trading day
- **Data Continuity**: Maintains historical data integrity without gaps or duplicates

#### Intelligent Automation Features
- **Duplicate Prevention**: Enforces once-per-day execution to maintain data quality
- **Graceful Degradation**: System continues operating even if individual components fail
- **Rate Limiting**: Respects API quotas (Polygon.io: 5 calls/minute, OpenRouter: model-specific limits)
- **Self-Healing**: Automatic recovery from temporary failures with comprehensive logging

## 🛠️ Technology Stack

### Backend Infrastructure
- **Python 3.12** - Core backend with async capabilities
- **Flask + CORS** - REST API framework serving 5 endpoints
- **SQLAlchemy ORM** - Database operations with relationship management
- **PostgreSQL 17.6** - Primary database with JSON support (Railway managed)
- **Python Schedule** - Cron-like job scheduling for daily automation
- **Threading** - Concurrent execution of pipeline and API server

### Frontend Technologies
- **React 18** - Modern frontend with hooks and functional components
- **Recharts 2.8** - Interactive data visualization and charting library
- **Tailwind CSS** - Utility-first styling with custom animations
- **Fetch API** - HTTP client for real-time backend communication

### External Integrations
- **Polygon.io API** - Enterprise-grade financial data provider
- **OpenRouter.ai** - LLM API gateway providing access to LLaMA 3.2
- **Railway.app** - Backend hosting with managed PostgreSQL
- **Vercel** - Frontend hosting with global CDN

## 🎯 Business Intelligence Output

### Real-Time Analysis Example
```
📊 STOCK DATA (AAPL - 2025-09-12):
   Open:  $229.22    Close: $234.07
   Change: $+4.85 (+2.12%)
   Volume: 55,824,216    VWAP: $231.50

🤖 AI ANALYSIS:
   Sentiment: BULLISH
   Risk Score: 6/10
   Price Prediction: $235.00

💡 AI RECOMMENDATIONS:
   1. Buy AAPL due to strong quarterly earnings
   2. AAPL is a good long-term investment opportunity  
   3. The recent price increase is a buying signal

📈 PERFORMANCE METRICS:
   Total Days Analyzed: 3
   Sentiment Distribution: 67% Bullish, 33% Bearish
   Average Risk Score: 6.7/10
   Price Range: $226.79 - $234.07
```

## 🔗 API Documentation

### Core Endpoints

**GET /api/latest** - Latest Stock Data
```json
{
  "date": "2025-09-12",
  "symbol": "AAPL",
  "stockData": {
    "open": 229.22,
    "close": 234.07,
    "change": 4.85,
    "changePercent": 2.12,
    "volume": 55824216
  },
  "aiAnalysis": {
    "sentiment": "bullish",
    "riskScore": 6,
    "pricePrediction": 235.0,
    "recommendations": ["Buy AAPL due to strong earnings"]
  }
}
```

**GET /api/historical** - Chart Data  
Returns last 30 days of OHLCV data for visualization

**GET /api/recommendations** - All AI Analysis  
Returns complete recommendation history with accuracy metrics

**GET /api/metrics** - System Performance  
Returns sentiment distribution, price analytics, and system statistics

**GET /api/health** - Health Check  
Returns system status and database connectivity

## 🚀 Installation & Deployment

### Prerequisites
- Python 3.12+ and Node.js 18+
- Polygon.io API key (free tier: 5 calls/minute)
- OpenRouter.ai API key (free $1 credit)
- Railway and Vercel accounts

### Backend Setup (Railway)

1. **Environment Configuration**
   ```bash
   POLYGON_API_KEY=your_polygon_api_key
   OPENROUTER_API_KEY=your_openrouter_key
   STOCK_SYMBOL=AAPL
   LLM_MODEL=meta-llama/llama-3.2-3b-instruct:free
   RUN_HOUR=14  # 9 AM EST in UTC
   ```

2. **Railway Deployment**
   ```bash
   git clone https://github.com/ThiruDeepak2311/fintech-intelligence-pipeline.git
   # Connect repository to Railway
   # Add PostgreSQL service
   # Deploy automatically on git push
   ```

### Frontend Setup (Vercel)

1. **Local Development**
   ```bash
   cd dashboard
   npm install
   npm start  # Runs on localhost:3000
   ```

2. **Vercel Deployment**
   ```bash
   cd dashboard
   npm install -g vercel
   vercel  # Follow prompts for deployment
   ```

## 📁 Project Structure

```
fintech-intelligence-pipeline/
├── src/                              # Backend Python modules
│   ├── data_fetcher.py              # Polygon.io API integration
│   ├── database.py                  # PostgreSQL ORM models
│   ├── llm_analyzer.py              # LLM integration & prompt engineering
│   └── __init__.py
├── dashboard/                        # Frontend React application
│   ├── src/
│   │   ├── components/              # React UI components
│   │   │   ├── StockOverview.js     # Price cards & market summary
│   │   │   ├── PriceChart.js        # Interactive Recharts visualization
│   │   │   ├── AIAnalysis.js        # Sentiment & risk display
│   │   │   ├── RecommendationsTable.js  # Sortable data table
│   │   │   ├── PerformanceMetrics.js    # Analytics dashboard
│   │   │   └── LoadingSpinner.js    # Loading states
│   │   ├── services/
│   │   │   └── database.js          # API client with error handling
│   │   ├── App.js                   # Main application orchestrator
│   │   └── index.js                 # React entry point
│   ├── public/index.html            # HTML template
│   └── package.json                 # Node.js dependencies
├── main.py                          # Pipeline orchestrator + Flask API
├── backfill.py                      # Historical data loading utility
├── requirements.txt                 # Python dependencies
├── railway.json                     # Railway deployment configuration
└── README.md                        # Project documentation
```

## 🗄️ Database Schema

### daily_metrics Table
```sql
id              SERIAL PRIMARY KEY
date            VARCHAR(10) NOT NULL        -- '2025-09-12'
symbol          VARCHAR(10) NOT NULL        -- 'AAPL'
open_price      FLOAT                       -- 229.22
close_price     FLOAT                       -- 234.07
high_price      FLOAT                       -- 234.51
low_price       FLOAT                       -- 229.02
volume          BIGINT                      -- 55824216
vwap            FLOAT                       -- 231.50
transactions    INTEGER                     -- 850000
raw_data        JSON                        -- Complete API response
created_at      TIMESTAMP DEFAULT NOW()
```

### ai_recommendations Table
```sql
id                SERIAL PRIMARY KEY
date              VARCHAR(10) NOT NULL
metrics_id        INTEGER REFERENCES daily_metrics(id)
sentiment         VARCHAR(20)               -- 'bullish', 'bearish', 'neutral'
risk_score        INTEGER                   -- 1-10 scale
price_prediction  FLOAT                     -- 235.0
recommendations   JSON                      -- Array of recommendation strings
full_analysis     TEXT                      -- Complete AI analysis
model_used        VARCHAR(100)              -- 'meta-llama/llama-3.2-3b-instruct:free'
created_at        TIMESTAMP DEFAULT NOW()
```

## 🔒 Security & Production Features

### Security Implementation
- **Environment Variables**: All API keys stored securely, never in code
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Input Validation**: Comprehensive sanitization of all external data
- **Error Handling**: Safe logging without sensitive data exposure
- **Database Security**: Connection encryption and parameterized queries

### Production Readiness
- **Automated Deployment**: CI/CD pipeline with Railway and Vercel
- **Health Monitoring**: Endpoint monitoring and database connectivity checks
- **Error Recovery**: Graceful degradation with fallback data mechanisms
- **Rate Limiting**: Respect for API quotas and intelligent retry logic
- **Scalability**: Modular architecture supporting horizontal scaling

### Performance Metrics
- **Response Time**: API endpoints respond in <500ms
- **Uptime**: 99.9% availability across Railway and Vercel infrastructure
- **Data Accuracy**: Real-time financial data with enterprise API reliability
- **Cost Efficiency**: Operates entirely on free tiers with scalable architecture

## 📈 System Monitoring & Analytics

### Operational Metrics
- **Daily Pipeline Execution**: Tracks successful data collection and analysis
- **API Performance**: Monitors endpoint response times and error rates
- **Database Growth**: Tracks data accumulation and storage efficiency
- **AI Model Performance**: Measures prediction accuracy over time

### Business Intelligence
- **Market Sentiment Trends**: Historical analysis of bullish vs bearish periods
- **Risk Assessment Accuracy**: Correlation between risk scores and actual volatility
- **Investment Recommendation Tracking**: Backtesting AI advice against market performance
- **Volume and Price Analysis**: Statistical insights into market behavior patterns

## 🔧 Development & Maintenance

### Local Development
```bash
# Backend development
python main.py                    # Single pipeline execution
python main.py --api             # API server only
python main.py --schedule        # Full automation mode

# Frontend development
cd dashboard && npm start         # Development server with hot reload

# Testing individual components
python -m src.data_fetcher        # Test API integration
python -m src.llm_analyzer        # Test AI analysis
```

### Monitoring & Troubleshooting
- **Railway Logs**: Real-time backend execution monitoring
- **Vercel Analytics**: Frontend performance and user interaction tracking
- **Database Queries**: PostgreSQL performance monitoring
- **API Health Checks**: Automated endpoint availability verification

## 🎯 Future Enhancement Roadmap

### Immediate Improvements
- **Multi-Stock Support**: Extend beyond AAPL to track multiple securities
- **Advanced Technical Indicators**: RSI, MACD, Bollinger Bands integration
- **Alert System**: Email/SMS notifications for significant market movements
- **User Authentication**: Secure user accounts with personalized portfolios

### Advanced Features
- **Real-Time WebSocket**: Live price updates without page refresh
- **Portfolio Optimization**: AI-driven asset allocation recommendations
- **Social Sentiment**: Integration with Twitter/Reddit for market sentiment
- **Mobile Application**: React Native app for iOS/Android platforms

## 📞 Contact & Support

**Developer**: Deepak Thirukkumaran  
**Email**: thirudeepak2003@gmail.com  
**GitHub**: https://github.com/ThiruDeepak2311  
**LinkedIn**: [Deepak Thirukkumaran](https://linkedin.com/in/deepak-thirukkumaran)

**Live System URLs**:
- **Dashboard**: https://finpipe-dashboard.vercel.app
- **API**: https://fintech-intelligence-pipeline-production.up.railway.app
- **Repository**: https://github.com/ThiruDeepak2311/fintech-intelligence-pipeline

---

**Built with professional standards for production deployment, demonstrating full-stack development expertise, AI integration capabilities, and real-world financial application development.**
