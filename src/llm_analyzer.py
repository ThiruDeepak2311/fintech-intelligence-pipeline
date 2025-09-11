import os
import json
import requests
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    def __init__(self):
        self.provider = os.getenv('LLM_PROVIDER', 'openrouter')
        self.model = os.getenv('LLM_MODEL', 'meta-llama/llama-3.2-3b-instruct:free')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
    def analyze_stock_data(self, stock_data):
        """
        Send stock data to LLM for analysis and recommendations
        """
        if not stock_data:
            return None
            
        # Prepare the prompt with stock data
        prompt = self._create_analysis_prompt(stock_data)
        
        # Get LLM response
        if self.provider == 'openrouter':
            response = self._call_openrouter(prompt)
        else:
            response = self._get_demo_analysis(stock_data)
            
        # Parse and structure the response
        return self._parse_llm_response(response, stock_data)
    
    def _create_analysis_prompt(self, data):
        """Create structured prompt for LLM analysis"""
        price_change = data['close_price'] - data['open_price']
        change_pct = (price_change / data['open_price']) * 100
        return f"""
You are a fintech analyst. Analyze this stock data and respond with VALID JSON only.

STOCK DATA:
- Symbol: {data['symbol']} on {data['date']}
- Open: ${data['open_price']:.2f}
- Close: ${data['close_price']:.2f}
- Change: ${price_change:+.2f} ({change_pct:+.2f}%)
- High: ${data['high_price']:.2f}
- Low: ${data['low_price']:.2f}
- Volume: {data['volume']:,}

RESPOND WITH VALID JSON ONLY (no extra text):

{{
    "sentiment": "bullish",
    "risk_score": 6,
    "recommendations": [
        "First recommendation",
        "Second recommendation", 
        "Third recommendation"
    ],
    "price_prediction": 225.50,
    "summary": "Brief analysis summary"
}}

Make sure recommendations are separate strings in the array, and sentiment matches the price movement."""

    def _call_openrouter(self, prompt):
        """Call OpenRouter API"""
        if not self.openrouter_key or self.openrouter_key == "your_openrouter_key_here":
            print("⚠️  No OpenRouter API key - using demo analysis")
            return None
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            print("🤖 Calling LLM for analysis...")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ LLM API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return None
    
    def _get_demo_analysis(self, data):
        """Demo analysis when no API key"""
        print("🔧 Demo mode: Generating sample analysis")
        
        # Simple logic for demo
        price_change = data['close_price'] - data['open_price']
        sentiment = "bullish" if price_change > 0 else "bearish" if price_change < 0 else "neutral"
        
        return json.dumps({
            "sentiment": sentiment,
            "risk_score": 5,
            "recommendations": [
                "Monitor volume trends for momentum confirmation",
                "Watch for price action near VWAP levels", 
                "Consider position sizing based on volatility"
            ],
            "price_prediction": round(data['close_price'] * 1.02, 2),
            "summary": f"Stock showed {sentiment} movement with ${price_change:.2f} change"
        })
    
    def _parse_llm_response(self, llm_response, stock_data):
        """Parse LLM response into structured format - ROBUST VERSION"""
        if not llm_response:
            llm_response = self._get_demo_analysis(stock_data)
            
        try:
            # Print raw response for debugging
            print(f"🔍 Raw LLM Response: {llm_response[:200]}...")
            
            # Try to parse JSON from response
            if isinstance(llm_response, str):
                # Multiple cleaning attempts
                cleaned = llm_response.strip()
                
                # Remove markdown code blocks
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0]
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0]
                
                # Try to find JSON-like content between braces
                json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
                if json_match:
                    cleaned = json_match.group()
                
                # Fix common JSON issues
                cleaned = cleaned.replace("'", '"')  # Single to double quotes
                cleaned = re.sub(r',\s*}', '}', cleaned)  # Remove trailing commas
                cleaned = re.sub(r',\s*]', ']', cleaned)  # Remove trailing commas in arrays
                
                print(f"🔧 Cleaned JSON: {cleaned[:200]}...")
                
                analysis = json.loads(cleaned)
            else:
                analysis = llm_response
                
            # Validate and extract fields
            sentiment = analysis.get('sentiment', 'neutral')
            if sentiment not in ['bullish', 'bearish', 'neutral']:
                sentiment = 'neutral'
                
            risk_score = analysis.get('risk_score', 5)
            if not isinstance(risk_score, int) or risk_score < 1 or risk_score > 10:
                risk_score = 5
                
            recommendations = analysis.get('recommendations', [])
            if not isinstance(recommendations, list) or len(recommendations) == 0:
                recommendations = ['Monitor market conditions', 'Review position sizing', 'Watch key levels']
                
            return {
                'sentiment': sentiment,
                'risk_score': risk_score,
                'recommendations': recommendations[:3],  # Limit to 3
                'price_prediction': analysis.get('price_prediction', stock_data['close_price']),
                'full_analysis': analysis.get('summary', analysis.get('analysis', 'Analysis completed')),
                'model_used': self.model,
                'raw_response': llm_response
            }
            
        except Exception as e:
            print(f"⚠️  JSON parsing failed: {e}")
            print(f"🔍 Problematic response: {llm_response}")
            
            # Enhanced fallback with actual data analysis
            price_change = stock_data['close_price'] - stock_data['open_price']
            change_pct = (price_change / stock_data['open_price']) * 100
            
            if change_pct > 2:
                sentiment = 'bullish'
                risk_score = 4
            elif change_pct < -2:
                sentiment = 'bearish'
                risk_score = 7
            else:
                sentiment = 'neutral'
                risk_score = 5
                
            return {
                'sentiment': sentiment,
                'risk_score': risk_score,
                'recommendations': [
                    f'Stock moved {change_pct:.1f}% - monitor for continuation',
                    'Consider volume analysis for confirmation',
                    'Watch key support/resistance levels'
                ],
                'price_prediction': round(stock_data['close_price'] * (1 + change_pct/100/10), 2),
                'full_analysis': f'Fallback analysis: {sentiment} sentiment based on {change_pct:.2f}% price movement',
                'model_used': f'{self.model}_fallback',
                'raw_response': str(llm_response)
            }

# Test function
def test_analyzer():
    print("🔧 Testing LLM analyzer with REAL stock data...")
    
    # Import our data fetcher to get REAL data
    import sys
    sys.path.append('.')
    from src.data_fetcher import PolygonDataFetcher
    from datetime import datetime, timedelta
    
    # Get REAL stock data from yesterday
    fetcher = PolygonDataFetcher()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    real_data = fetcher.fetch_daily_data('AAPL', yesterday)
    
    if not real_data:
        print("❌ Could not fetch real data for testing")
        return False
    
    print(f"📊 Using REAL data: Open ${real_data['open_price']} → Close ${real_data['close_price']}")
    
    analyzer = LLMAnalyzer()
    analysis = analyzer.analyze_stock_data(real_data)
    
    if analysis:
        print("✅ Analysis completed!")
        print(f"Sentiment: {analysis['sentiment']}")
        print(f"Risk Score: {analysis['risk_score']}")
        print(f"Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
        print(f"Model Used: {analysis['model_used']}")
        return True
    else:
        print("❌ Analysis failed")
        return False

if __name__ == "__main__":
    test_analyzer()