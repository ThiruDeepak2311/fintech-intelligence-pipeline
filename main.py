import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path so we can import our modules
sys.path.append('src')

from data_fetcher import PolygonDataFetcher
from database import DatabaseManager, DailyMetrics, AIRecommendations
from llm_analyzer import LLMAnalyzer

load_dotenv()

class FintechPipeline:
    def __init__(self):
        self.fetcher = PolygonDataFetcher()
        self.db = DatabaseManager()
        self.analyzer = LLMAnalyzer()
        self.symbol = os.getenv('STOCK_SYMBOL', 'AAPL')
        
    def run_daily_pipeline(self, target_date=None):
        """
        Run the complete pipeline for a specific date
        If no date provided, uses yesterday
        """
        if not target_date:
            target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
        print(f"\n🚀 Starting pipeline for {self.symbol} on {target_date}")
        print("=" * 50)
        
        # Step 1: Fetch stock data
        print("📡 Step 1: Fetching stock data...")
        stock_data = self.fetcher.fetch_daily_data(self.symbol, target_date)
        
        if not stock_data:
            print("❌ Failed to fetch stock data. Aborting pipeline.")
            return False
            
        print(f"✅ Stock data fetched: ${stock_data['close_price']}")
        
        # Step 2: Store in database
        print("\n💾 Step 2: Storing data in database...")
        try:
            session = self.db.get_session()
            
            # Create daily metrics record
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
            print(f"✅ Data stored with ID: {metrics_id}")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            print("⚠️  Continuing with in-memory analysis...")
            metrics_id = None
            session = None
        
        # Step 3: LLM Analysis
        print("\n🤖 Step 3: Generating LLM analysis...")
        analysis = self.analyzer.analyze_stock_data(stock_data)
        
        if not analysis:
            print("❌ Failed to generate analysis. Aborting.")
            return False
            
        print(f"✅ Analysis completed - Sentiment: {analysis['sentiment']}")
        
        # Step 4: Store AI recommendations
        print("\n📊 Step 4: Storing AI recommendations...")
        try:
            if session and metrics_id:
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
                print("✅ AI recommendations stored!")
            else:
                print("⚠️  Skipped database storage (no connection)")
                
        except Exception as e:
            print(f"❌ Failed to store recommendations: {e}")
        
        # Step 5: Display results
        self._display_results(stock_data, analysis)
        
        print("\n🎉 Pipeline completed successfully!")
        return True
    
    def _display_results(self, stock_data, analysis):
        """Display pipeline results in a nice format"""
        print("\n" + "="*50)
        print("📈 DAILY FINTECH INTELLIGENCE REPORT")
        print("="*50)
        
        print(f"\n📊 STOCK DATA ({stock_data['symbol']} - {stock_data['date']}):")
        print(f"   Open:  ${stock_data['open_price']}")
        print(f"   Close: ${stock_data['close_price']}")
        print(f"   High:  ${stock_data['high_price']}")
        print(f"   Low:   ${stock_data['low_price']}")
        print(f"   Volume: {stock_data['volume']:,}")
        
        price_change = stock_data['close_price'] - stock_data['open_price']
        change_pct = (price_change / stock_data['open_price']) * 100
        print(f"   Change: ${price_change:+.2f} ({change_pct:+.2f}%)")
        
        print(f"\n🤖 AI ANALYSIS:")
        print(f"   Sentiment: {analysis['sentiment'].upper()}")
        print(f"   Risk Score: {analysis['risk_score']}/10")
        print(f"   Price Prediction: ${analysis['price_prediction']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
            
        print(f"\n📝 Summary: {analysis['full_analysis']}")
        print("="*50)

def main():
    """Main entry point"""
    print("🏦 FINTECH INTELLIGENCE PIPELINE")
    print("Fetching → Storing → Analyzing → Recommending")
    
    # Initialize pipeline
    pipeline = FintechPipeline()
    
    # Create database tables (if not exists)
    try:
        pipeline.db.create_tables()
    except Exception as e:
        print(f"⚠️  Database setup skipped: {e}")
        print("📝 Note: Pipeline will run in analysis-only mode")
    
    # Run pipeline
    success = pipeline.run_daily_pipeline()
    
    if success:
        print("\n✅ All systems operational!")
    else:
        print("\n❌ Pipeline encountered errors.")

if __name__ == "__main__":
    main()