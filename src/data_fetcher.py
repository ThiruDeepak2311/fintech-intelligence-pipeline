import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

class PolygonDataFetcher:
    """
    DATA FETCHER CLASS - The Stock Data Collector
    
    PURPOSE: Connects to Polygon.io API to fetch real-time stock market data
    BUSINESS VALUE: Provides fresh financial data for AI analysis and investment decisions
    
    This class acts as our "data delivery service" - it knows how to:
    1. Connect to Polygon.io financial API
    2. Request specific stock data for any date
    3. Handle errors gracefully if API is unavailable
    4. Format raw API response into clean, usable data structure
    """
    
    def __init__(self):
        """
        CONSTRUCTOR - Set up the data fetcher with API credentials
        
        WHY WE DO THIS:
        - Get API key from environment variables (secure storage)
        - Set up the base URL for Polygon.io API calls
        - Prepare for making authenticated requests to financial data service
        """
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io/v1/open-close"
        
    def fetch_daily_data(self, symbol, date):
        """
        MAIN METHOD - Fetch complete daily stock data for a specific symbol and date
        
        PARAMETERS:
        - symbol: Stock ticker (e.g., 'AAPL' for Apple)
        - date: Date in YYYY-MM-DD format (e.g., '2025-09-10')
        
        RETURNS:
        Dictionary with complete stock data or None if failed
        
        BUSINESS PURPOSE:
        - Get yesterday's complete market data for AI analysis
        - Ensure we have all key metrics: open, close, high, low, volume
        - Provide foundation data for investment recommendations
        """
        
        # SAFETY CHECK: If no API key available, use demo mode
        if not self.api_key or self.api_key == "your_polygon_key_here":
            print("Warning: Using demo mode - need real API key for live data")
            return self._get_demo_data(symbol, date)
            
        # BUILD THE API REQUEST
        # Example: https://api.polygon.io/v1/open-close/AAPL/2025-09-10?apikey=xxx
        url = f"{self.base_url}/{symbol}/{date}"
        params = {"apikey": self.api_key}
        
        try:
            print(f"Fetching data for {symbol} on {date}...")
            response = requests.get(url, params=params)
            
            # CHECK IF API CALL WAS SUCCESSFUL
            if response.status_code == 200:
                data = response.json()
                
                # VALIDATE API RESPONSE
                if data.get('status') == 'OK':
                    return self._format_data(data, symbol, date)
                else:
                    print(f"API Error: {data.get('error', 'Unknown error')}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def _format_data(self, raw_data, symbol, date):
        """
        DATA FORMATTER - Convert raw API response into clean, structured format
        
        PURPOSE:
        - Transform Polygon.io's response format into our standard data structure
        - Ensure consistent field names across our system
        - Store both processed data and raw response for debugging
        
        INPUT: Raw JSON from Polygon.io API
        OUTPUT: Clean dictionary with standardized field names
        
        WHY THIS MATTERS:
        - Our database and AI analyzer expect consistent field names
        - If Polygon.io changes their format, we only need to update this one function
        - Provides data validation and type consistency
        """
        return {
            'date': date,
            'symbol': symbol,
            'open_price': raw_data.get('open'),          # Market opening price
            'close_price': raw_data.get('close'),        # Market closing price  
            'high_price': raw_data.get('high'),          # Highest price of the day
            'low_price': raw_data.get('low'),            # Lowest price of the day
            'volume': raw_data.get('volume'),            # Number of shares traded
            'vwap': raw_data.get('vwap'),               # Volume-weighted average price
            'transactions': raw_data.get('transactions', 0),  # Number of individual trades
            'raw_data': raw_data                         # Store complete API response for debugging
        }
    
    def _get_demo_data(self, symbol, date):
        """
        DEMO MODE - Provide realistic sample data when no API key is available
        
        PURPOSE:
        - Enable development and testing without real API access
        - Provide realistic data that mimics real market behavior
        - Allow system to run end-to-end even without API credentials
        
        WHY THIS IS IMPORTANT:
        - Developers can work on other parts of system without API keys
        - System can be demonstrated even if API is temporarily unavailable
        - Provides fallback for graceful degradation in production
        """
        print(f"Demo mode: Generating sample data for {symbol}")
        return {
            'date': date,
            'symbol': symbol,
            'open_price': 150.25,      # Realistic opening price
            'close_price': 152.80,     # Small price movement (bullish)
            'high_price': 154.20,      # Day's high price
            'low_price': 149.50,       # Day's low price
            'volume': 25000000,        # Typical daily volume
            'vwap': 151.75,           # Volume-weighted average
            'transactions': 85000,     # Number of trades
            'raw_data': {'status': 'demo_data'}  # Mark as demo data
        }

# TESTING FUNCTION - Verify the data fetcher works correctly
def test_fetcher():
    """
    TEST FUNCTION - Validate that data fetching works correctly
    
    PURPOSE:
    - Test API connection and data retrieval
    - Verify data format is correct
    - Provide quick validation during development
    
    USAGE: Run this file directly to test data fetching
    """
    print("Testing data fetcher...")
    fetcher = PolygonDataFetcher()
    
    # Test with yesterday's date (markets are closed, data is complete)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    data = fetcher.fetch_daily_data('AAPL', yesterday)
    
    if data:
        print("Data fetched successfully!")
        print(f"Sample: {data['symbol']} - Close: ${data['close_price']}")
        return True
    else:
        print("Failed to fetch data")
        return False

# RUN TEST IF FILE IS EXECUTED DIRECTLY
if __name__ == "__main__":
    test_fetcher()