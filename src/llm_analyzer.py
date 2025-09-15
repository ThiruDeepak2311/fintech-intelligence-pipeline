import os
import json
import requests
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMAnalyzer:
    """
    LLM ANALYZER CLASS - The AI-Powered Financial Intelligence Engine
    
    PURPOSE: Transform raw stock data into actionable business intelligence using AI
    BUSINESS VALUE: Provides professional investment analysis and recommendations
    
    KEY CAPABILITIES:
    - Sentiment analysis (bullish/bearish/neutral market mood)
    - Risk quantification (1-10 scoring system)
    - Investment recommendations (buy/sell/hold advice)
    - Price predictions (where AI thinks stock is heading)
    
    WHY AI ANALYSIS MATTERS:
    - Processes complex market data faster than human analysts
    - Identifies patterns humans might miss
    - Provides consistent, objective analysis without emotional bias
    - Available 24/7 for real-time market intelligence
    """
    
    def __init__(self):
        """
        CONSTRUCTOR - Set up AI analyzer with provider configuration
        
        PURPOSE:
        - Configure which AI service to use (OpenRouter with LLaMA)
        - Set up API credentials for AI model access
        - Choose specific model for financial analysis
        
        DESIGN DECISION - Why LLaMA 3.2 via OpenRouter:
        - Cost-effective (free tier available)
        - High-quality analysis comparable to GPT-4
        - Specialized for instruction-following tasks
        - Professional API with good reliability
        """
        self.provider = os.getenv('LLM_PROVIDER', 'openrouter')
        self.model = os.getenv('LLM_MODEL', 'meta-llama/llama-3.2-3b-instruct:free')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
    def analyze_stock_data(self, stock_data):
        """
        MAIN ANALYSIS METHOD - Convert stock data into AI-powered business intelligence
        
        PARAMETERS:
        - stock_data: Dictionary with OHLC prices, volume, etc. from data_fetcher.py
        
        RETURNS:
        Dictionary with sentiment, risk score, recommendations, predictions
        
        BUSINESS PROCESS:
        1. Create structured prompt with stock data
        2. Send to AI model for analysis
        3. Parse AI response into structured format
        4. Validate and clean the results
        5. Return actionable business intelligence
        
        EXAMPLE INPUT: AAPL open $232.185, close $226.79 (-2.32%)
        EXAMPLE OUTPUT: Bearish sentiment, risk score 8, sell recommendations
        """
        if not stock_data:
            return None
            
        # STEP 1: Create structured prompt for AI analysis
        prompt = self._create_analysis_prompt(stock_data)
        
        # STEP 2: Send to appropriate AI provider
        if self.provider == 'openrouter':
            response = self._call_openrouter(prompt)
        else:
            response = self._get_demo_analysis(stock_data)
            
        # STEP 3: Parse and structure the AI response
        return self._parse_llm_response(response, stock_data)
    
    def _create_analysis_prompt(self, data):
        """
        PROMPT ENGINEERING - Create structured request for AI financial analysis
        
        PURPOSE:
        - Format stock data into clear, analyzable format for AI
        - Request specific output format (JSON) for reliable parsing
        - Include context about financial analysis requirements
        - Calculate key metrics (price change %) for AI consideration
        
        PROMPT STRATEGY:
        - Role definition: "You are a fintech analyst"
        - Clear data presentation with calculated metrics
        - Specific output format request (JSON only)
        - Professional financial terminology requirements
        
        WHY THIS APPROACH WORKS:
        - AI models respond better to structured, role-based prompts
        - JSON format ensures machine-readable responses
        - Calculated metrics help AI understand market movement significance
        """
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
        """
        OPENROUTER API INTEGRATION - Send analysis request to LLaMA AI model
        
        PURPOSE:
        - Connect to OpenRouter.ai service for AI model access
        - Send structured financial analysis prompt
        - Handle API authentication and response processing
        - Manage timeouts and error conditions
        
        API DETAILS:
        - Endpoint: https://openrouter.ai/api/v1/chat/completions
        - Model: meta-llama/llama-3.2-3b-instruct:free
        - Max tokens: 500 (sufficient for structured JSON response)
        - Temperature: 0.7 (balanced creativity vs consistency)
        
        BUSINESS VALUE:
        - Access to enterprise-grade AI models
        - Cost-effective analysis (free tier available)
        - Reliable API with good uptime
        - Professional service suitable for production use
        """
        # SAFETY CHECK: Verify API key is available
        if not self.openrouter_key or self.openrouter_key == "your_openrouter_key_here":
            print("Warning: No OpenRouter API key - using demo analysis")
            return None
            
        # API CONFIGURATION
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        # REQUEST PARAMETERS
        data = {
            "model": self.model,                    # LLaMA 3.2 model
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,                      # Limit response length
            "temperature": 0.7                      # Balance creativity/consistency
        }
        
        try:
            print("Calling LLM for financial analysis...")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"LLM API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"LLM Error: {e}")
            return None
    
    def _get_demo_analysis(self, data):
        """
        DEMO MODE ANALYSIS - Provide realistic sample analysis when no API key
        
        PURPOSE:
        - Enable system testing without real API access
        - Provide intelligent fallback based on actual price movement
        - Maintain system functionality during development
        - Demonstrate expected output format
        
        INTELLIGENT LOGIC:
        - Analyzes actual price change direction
        - Maps price movement to appropriate sentiment
        - Provides realistic recommendations based on market behavior
        - Maintains professional analysis quality
        """
        print("Demo mode: Generating intelligent sample analysis")
        
        # CALCULATE ACTUAL PRICE MOVEMENT for realistic analysis
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
        """
        RESPONSE PARSER - Robust processing of AI analysis into structured format
        
        PURPOSE:
        - Handle various AI response formats (clean JSON, markdown, etc.)
        - Validate AI output quality and consistency
        - Provide intelligent fallbacks for parsing failures
        - Ensure business-ready data structure
        
        PARSING CHALLENGES SOLVED:
        - AI sometimes wraps JSON in markdown code blocks
        - Responses may include extra text before/after JSON
        - JSON may have syntax errors (trailing commas, single quotes)
        - Sentiment values may be non-standard formats
        
        ROBUST ERROR HANDLING:
        - Multiple cleaning attempts with regex patterns
        - Data validation for business logic compliance
        - Intelligent fallback analysis using price movement rules
        - Comprehensive error logging for debugging
        """
        if not llm_response:
            llm_response = self._get_demo_analysis(stock_data)
            
        try:
            # DEBUG: Print raw response for troubleshooting
            print(f"Raw LLM Response: {llm_response[:200]}...")
            
            # STEP 1: Clean the response string
            if isinstance(llm_response, str):
                cleaned = llm_response.strip()
                
                # Remove markdown code blocks (```json ... ```)
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0]
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0]
                
                # Extract JSON content using regex
                json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
                if json_match:
                    cleaned = json_match.group()
                
                # Fix common JSON formatting issues
                cleaned = cleaned.replace("'", '"')           # Single to double quotes
                cleaned = re.sub(r',\s*}', '}', cleaned)      # Remove trailing commas
                cleaned = re.sub(r',\s*]', ']', cleaned)      # Remove trailing commas in arrays
                
                print(f"Cleaned JSON: {cleaned[:200]}...")
                
                analysis = json.loads(cleaned)
            else:
                analysis = llm_response
                
            # STEP 2: Validate and extract business data
            
            # SENTIMENT VALIDATION - Ensure valid financial sentiment
            sentiment = analysis.get('sentiment', 'neutral')
            if sentiment not in ['bullish', 'bearish', 'neutral']:
                sentiment = 'neutral'
                
            # RISK SCORE VALIDATION - Ensure valid 1-10 scale
            risk_score = analysis.get('risk_score', 5)
            if not isinstance(risk_score, int) or risk_score < 1 or risk_score > 10:
                risk_score = 5
                
            # RECOMMENDATIONS VALIDATION - Ensure usable advice list
            recommendations = analysis.get('recommendations', [])
            if not isinstance(recommendations, list) or len(recommendations) == 0:
                recommendations = ['Monitor market conditions', 'Review position sizing', 'Watch key levels']
                
            # RETURN STRUCTURED BUSINESS INTELLIGENCE
            return {
                'sentiment': sentiment,
                'risk_score': risk_score,
                'recommendations': recommendations[:3],  # Limit to top 3 recommendations
                'price_prediction': analysis.get('price_prediction', stock_data['close_price']),
                'full_analysis': analysis.get('summary', analysis.get('analysis', 'Analysis completed')),
                'model_used': self.model,
                'raw_response': llm_response
            }
            
        except Exception as e:
            print(f"JSON parsing failed: {e}")
            print(f"Problematic response: {llm_response}")
            
            # INTELLIGENT FALLBACK - Rule-based analysis using actual market data
            price_change = stock_data['close_price'] - stock_data['open_price']
            change_pct = (price_change / stock_data['open_price']) * 100
            
            # MARKET MOVEMENT ANALYSIS
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

# TESTING FUNCTION - Comprehensive validation with real market data
def test_analyzer():
    """
    TEST FUNCTION - Validate LLM analyzer with actual stock data
    
    PURPOSE:
    - Test complete analysis pipeline with real market data
    - Validate AI integration and response processing
    - Demonstrate business intelligence generation
    - Provide development and deployment validation
    
    TESTING STRATEGY:
    - Use real data from data_fetcher.py
    - Test with recent market data (yesterday's close)
    - Validate all output components (sentiment, risk, recommendations)
    - Display results in business-readable format
    """
    print("Testing LLM analyzer with REAL stock data...")
    
    # Import data fetcher to get real market data
    import sys
    sys.path.append('.')
    from src.data_fetcher import PolygonDataFetcher
    from datetime import datetime, timedelta
    
    # GET REAL STOCK DATA from yesterday
    fetcher = PolygonDataFetcher()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    real_data = fetcher.fetch_daily_data('AAPL', yesterday)
    
    if not real_data:
        print("Could not fetch real data for testing")
        return False
    
    print(f"Using REAL data: Open ${real_data['open_price']} → Close ${real_data['close_price']}")
    
    # PERFORM AI ANALYSIS
    analyzer = LLMAnalyzer()
    analysis = analyzer.analyze_stock_data(real_data)
    
    if analysis:
        print("Analysis completed successfully!")
        print(f"Sentiment: {analysis['sentiment']}")
        print(f"Risk Score: {analysis['risk_score']}")
        print(f"Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
        print(f"Model Used: {analysis['model_used']}")
        return True
    else:
        print("Analysis failed")
        return False

# RUN TEST IF FILE IS EXECUTED DIRECTLY
if __name__ == "__main__":
    test_analyzer()