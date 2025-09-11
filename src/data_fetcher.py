import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

load_dotenv()

class PolygonDataFetcher:
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io/v1/open-close"
        
    def fetch_daily_data(self, symbol, date):
        """
        Fetch OHLCV data for a specific symbol and date
        Format: YYYY-MM-DD
        """
        if not self.api_key or self.api_key == "your_polygon_key_here":
            print("⚠️  Using demo mode - need real API key for live data")
            return self._get_demo_data(symbol, date)
            
        url = f"{self.base_url}/{symbol}/{date}"
        params = {"apikey": self.api_key}
        
        try:
            print(f"📡 Fetching data for {symbol} on {date}...")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    return self._format_data(data, symbol, date)
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def _format_data(self, raw_data, symbol, date):
        """Format API response into our schema"""
        return {
            'date': date,
            'symbol': symbol,
            'open_price': raw_data.get('open'),
            'close_price': raw_data.get('close'), 
            'high_price': raw_data.get('high'),
            'low_price': raw_data.get('low'),
            'volume': raw_data.get('volume'),
            'vwap': raw_data.get('vwap'),
            'transactions': raw_data.get('transactions', 0),
            'raw_data': raw_data
        }
    
    def _get_demo_data(self, symbol, date):
        """Demo data when no API key"""
        print(f"🔧 Demo mode: Generating sample data for {symbol}")
        return {
            'date': date,
            'symbol': symbol,
            'open_price': 150.25,
            'close_price': 152.80,
            'high_price': 154.20,
            'low_price': 149.50,
            'volume': 25000000,
            'vwap': 151.75,
            'transactions': 85000,
            'raw_data': {'status': 'demo_data'}
        }

# Test function
def test_fetcher():
    print("🔧 Testing data fetcher...")
    fetcher = PolygonDataFetcher()
    
    # Test with yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    data = fetcher.fetch_daily_data('AAPL', yesterday)
    
    if data:
        print("✅ Data fetched successfully!")
        print(f"Sample: {data['symbol']} - Close: ${data['close_price']}")
        return True
    else:
        print("❌ Failed to fetch data")
        return False

if __name__ == "__main__":
    test_fetcher()