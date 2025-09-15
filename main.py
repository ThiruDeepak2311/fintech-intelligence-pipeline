import os
import sys
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# Add src directory to Python path for importing our custom modules
sys.path.append('src')

from data_fetcher import PolygonDataFetcher
from database import DatabaseManager, DailyMetrics, AIRecommendations
from llm_analyzer import LLMAnalyzer

load_dotenv()

# Initialize Flask app for API endpoints
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for React frontend

class FintechPipeline:
    """
    FINTECH INTELLIGENCE PIPELINE - Now with Flask API endpoints
    """
    
    def __init__(self):
        self.fetcher = PolygonDataFetcher()
        self.db = DatabaseManager()
        self.analyzer = LLMAnalyzer()
        self.symbol = os.getenv('STOCK_SYMBOL', 'AAPL')
        
    def _data_already_exists(self, target_date, symbol=None):
        """DUPLICATE PREVENTION - Check if data already exists for this date"""
        if not self.db.is_connected():
            return False
            
        if symbol is None:
            symbol = self.symbol
            
        try:
            session = self.db.get_session()
            existing = session.query(DailyMetrics).filter(
                DailyMetrics.date == target_date,
                DailyMetrics.symbol == symbol
            ).first()
            session.close()
            
            if existing:
                print(f"Data already exists for {symbol} on {target_date}")
                return True
            return False
            
        except Exception as e:
            print(f"Error checking existing data: {e}")
            return False
    
    def run_daily_pipeline(self, target_date=None, force_rerun=False):
        """MAIN PIPELINE EXECUTION - Complete daily intelligence generation process"""
        if not target_date:
            target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
        print(f"\nStarting pipeline for {self.symbol} on {target_date}")
        print("=" * 50)
        
        # DUPLICATE CHECK - Enforce once-per-day execution
        if not force_rerun and self._data_already_exists(target_date):
            print(f"SKIPPED: Data for {target_date} already processed today.")
            return True
        
        # STEP 1: FETCH STOCK DATA
        print("Step 1: Fetching stock data...")
        stock_data = self.fetcher.fetch_daily_data(self.symbol, target_date)
        
        if not stock_data:
            print("Failed to fetch stock data. Aborting pipeline.")
            return False
            
        print(f"Stock data fetched: ${stock_data['close_price']}")
        
        # STEP 2: STORE RAW DATA
        print("\nStep 2: Storing data in database...")
        metrics_id = None
        session = None
        
        try:
            if self.db.is_connected():
                session = self.db.get_session()
                
                metrics = DailyMetrics(
                    date=stock_data['date'],
                    symbol=stock_data['symbol'],
                    open_price=stock_data['open_price'],
                    close_price=stock_data['close_price'],
                    high_price=stock_data['high_price'],
                    low_price=stock_data['low_price'],
                    volume=stock_data['volume'],
                    vwap=stock_data['vwap'],
                    transactions=stock_data['transactions'],
                    raw_data=stock_data['raw_data']
                )
                
                session.add(metrics)
                session.commit()
                metrics_id = metrics.id
                print(f"Data stored with ID: {metrics_id}")
            else:
                print("Database not available - skipping storage")
                
        except Exception as e:
            print(f"Database error: {e}")
            if session:
                session.rollback()
        
        # STEP 3: AI ANALYSIS
        print("\nStep 3: Generating LLM analysis...")
        analysis = self.analyzer.analyze_stock_data(stock_data)
        
        if not analysis:
            print("Failed to generate analysis. Aborting.")
            return False
            
        print(f"Analysis completed - Sentiment: {analysis['sentiment']}")
        
        # STEP 4: STORE AI RECOMMENDATIONS
        print("\nStep 4: Storing AI recommendations...")
        try:
            if session and metrics_id and self.db.is_connected():
                recommendation = AIRecommendations(
                    date=target_date,
                    metrics_id=metrics_id,
                    sentiment=analysis['sentiment'],
                    recommendations=analysis['recommendations'],
                    risk_score=analysis['risk_score'],
                    price_prediction=analysis['price_prediction'],
                    full_analysis=analysis['full_analysis'],
                    model_used=analysis['model_used']
                )
                
                session.add(recommendation)
                session.commit()
                session.close()
                print("AI recommendations stored!")
            else:
                print("Skipped database storage (no connection)")
                
        except Exception as e:
            print(f"Failed to store recommendations: {e}")
            if session:
                session.close()
        
        # STEP 5: DISPLAY RESULTS
        self._display_results(stock_data, analysis)
        
        print(f"\nPipeline completed successfully for {target_date}!")
        return True
    
    def _display_results(self, stock_data, analysis):
        """BUSINESS INTELLIGENCE REPORTER"""
        print("\n" + "="*50)
        print("DAILY FINTECH INTELLIGENCE REPORT")
        print("="*50)
        
        print(f"\nSTOCK DATA ({stock_data['symbol']} - {stock_data['date']}):")
        print(f"   Open:  ${stock_data['open_price']}")
        print(f"   Close: ${stock_data['close_price']}")
        print(f"   High:  ${stock_data['high_price']}")
        print(f"   Low:   ${stock_data['low_price']}")
        print(f"   Volume: {stock_data['volume']:,}")
        
        price_change = stock_data['close_price'] - stock_data['open_price']
        change_pct = (price_change / stock_data['open_price']) * 100
        print(f"   Change: ${price_change:+.2f} ({change_pct:+.2f}%)")
        
        print(f"\nAI ANALYSIS:")
        print(f"   Sentiment: {analysis['sentiment'].upper()}")
        print(f"   Risk Score: {analysis['risk_score']}/10")
        print(f"   Price Prediction: ${analysis['price_prediction']}")
        
        print(f"\nRECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
            
        print(f"\nSummary: {analysis['full_analysis']}")
        print("="*50)

# Initialize pipeline instance
pipeline = FintechPipeline()

# =================================================================
# FLASK API ENDPOINTS FOR REACT FRONTEND
# =================================================================

@app.route('/api/latest')
def get_latest():
    """Get latest stock data with AI analysis"""
    try:
        if not pipeline.db.is_connected():
            return jsonify({'error': 'Database not available'}), 500
            
        session = pipeline.db.get_session()
        latest = session.query(DailyMetrics).order_by(DailyMetrics.id.desc()).first()
        
        if not latest:
            session.close()
            return jsonify({'error': 'No data available'}), 404
            
        ai = session.query(AIRecommendations).filter(AIRecommendations.metrics_id == latest.id).first()
        session.close()
        
        response = {
            'date': latest.date,
            'symbol': latest.symbol,
            'stockData': {
                'open': float(latest.open_price),
                'close': float(latest.close_price),
                'high': float(latest.high_price),
                'low': float(latest.low_price),
                'volume': int(latest.volume),
                'vwap': float(latest.vwap),
                'transactions': int(latest.transactions),
                'change': float(latest.close_price - latest.open_price),
                'changePercent': float(((latest.close_price - latest.open_price) / latest.open_price) * 100)
            }
        }
        
        if ai:
            response['aiAnalysis'] = {
                'sentiment': ai.sentiment,
                'riskScore': ai.risk_score,
                'pricePrediction': float(ai.price_prediction),
                'recommendations': ai.recommendations,
                'analysis': ai.full_analysis,
                'model': ai.model_used
            }
            
        return jsonify(response)
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/api/historical')
def get_historical():
    """Get historical stock data for charts"""
    try:
        if not pipeline.db.is_connected():
            return jsonify([])
            
        session = pipeline.db.get_session()
        data = session.query(DailyMetrics).order_by(DailyMetrics.date.desc()).limit(30).all()
        session.close()
        
        result = []
        for item in reversed(data):  # Reverse for chronological order
            result.append({
                'date': item.date,
                'open': float(item.open_price),
                'close': float(item.close_price),
                'high': float(item.high_price),
                'low': float(item.low_price),
                'volume': int(item.volume),
                'vwap': float(item.vwap)
            })
        return jsonify(result)
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify([])

@app.route('/api/recommendations')
def get_recommendations():
    """Get all AI recommendations with stock context"""
    try:
        if not pipeline.db.is_connected():
            return jsonify([])
            
        session = pipeline.db.get_session()
        results = session.query(AIRecommendations, DailyMetrics).join(
            DailyMetrics, AIRecommendations.metrics_id == DailyMetrics.id
        ).order_by(AIRecommendations.date.desc()).all()
        session.close()
        
        data = []
        for ai, metrics in results:
            change_pct = ((metrics.close_price - metrics.open_price) / metrics.open_price) * 100
            accuracy = max(0, 100 - abs((ai.price_prediction - metrics.close_price) / metrics.close_price * 100))
            
            data.append({
                'date': ai.date,
                'symbol': metrics.symbol,
                'sentiment': ai.sentiment,
                'riskScore': ai.risk_score,
                'pricePrediction': float(ai.price_prediction),
                'actualPrice': float(metrics.close_price),
                'recommendations': ai.recommendations,
                'changePercent': float(change_pct),
                'predictionAccuracy': float(accuracy)
            })
        return jsonify(data)
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify([])

@app.route('/api/metrics')
def get_metrics():
    """Get system performance metrics"""
    try:
        if not pipeline.db.is_connected():
            return jsonify({'error': 'Database not available'}), 500
            
        session = pipeline.db.get_session()
        
        # Count records
        total_days = session.query(DailyMetrics).count()
        total_recs = session.query(AIRecommendations).count()
        
        # Get sentiment distribution
        sentiments = session.query(AIRecommendations.sentiment).all()
        sentiment_counts = {}
        for (s,) in sentiments:
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1
        
        # Get price metrics
        prices = session.query(DailyMetrics.close_price, DailyMetrics.volume).all()
        
        # Get average risk score
        risk_scores = session.query(AIRecommendations.risk_score).all()
        avg_risk = sum([r[0] for r in risk_scores]) / len(risk_scores) if risk_scores else 0
        
        session.close()
        
        close_prices = [float(p[0]) for p in prices]
        volumes = [int(p[1]) for p in prices]
        
        return jsonify({
            'totalDaysAnalyzed': total_days,
            'totalRecommendations': total_recs,
            'sentimentDistribution': sentiment_counts,
            'averageRiskScore': round(avg_risk, 2),
            'priceMetrics': {
                'minPrice': min(close_prices) if close_prices else 0,
                'maxPrice': max(close_prices) if close_prices else 0,
                'avgPrice': sum(close_prices) / len(close_prices) if close_prices else 0,
                'avgVolume': sum(volumes) / len(volumes) if volumes else 0
            }
        })
        
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database_connected': pipeline.db.is_connected()
    })

# =================================================================
# SCHEDULING FUNCTIONS (unchanged)
# =================================================================

def run_single_pipeline(force_rerun=False):
    """SINGLE EXECUTION MODE"""
    print("FINTECH INTELLIGENCE PIPELINE")
    print("Fetching → Storing → Analyzing → Recommending")
    
    # DATABASE SETUP
    try:
        if pipeline.db.is_connected():
            pipeline.db.create_tables()
        else:
            print("Note: Pipeline will run in analysis-only mode")
    except Exception as e:
        print(f"Database setup skipped: {e}")
    
    # EXECUTE PIPELINE
    success = pipeline.run_daily_pipeline(force_rerun=force_rerun)
    
    if success:
        print("\nAll systems operational!")
    else:
        print("\nPipeline encountered errors.")

def run_daily_automation():
    """DAILY AUTOMATION TRIGGER"""
    print(f"Daily automation triggered at {datetime.now()}")
    run_single_pipeline()

def start_automation():
    """AUTOMATION SCHEDULER"""
    run_hour = int(os.getenv('RUN_HOUR', 14))
    schedule.every().day.at(f"{run_hour:02d}:00").do(run_daily_automation)
    
    print(f"Daily automation scheduled for {run_hour}:00 UTC (9 AM EST)")
    
    # Initial run
    run_single_pipeline()
    
    # Continuous operation
    print("Scheduler active - waiting for next scheduled run...")
    while True:
        schedule.run_pending()
        time.sleep(3600)

def run_api_server():
    """Run Flask API server"""
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

# =================================================================
# MAIN EXECUTION LOGIC
# =================================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schedule":
            # Production mode: Run both pipeline and API
            print("Starting combined pipeline + API server...")
            api_thread = threading.Thread(target=run_api_server, daemon=True)
            api_thread.start()
            start_automation()  # This runs forever
        elif sys.argv[1] == "--api":
            # API only mode
            run_api_server()
        elif sys.argv[1] == "--force":
            run_single_pipeline(force_rerun=True)
        else:
            print("Invalid argument. Use --schedule, --api, or --force")
    else:
        run_single_pipeline()