// Real API integration with Railway backend
const API_BASE_URL = 'https://fintech-intelligence-pipeline-production.up.railway.app';

class DatabaseService {
  constructor() {
    console.log('DatabaseService initialized with real API:', API_BASE_URL);
  }

  async getLatestStockData() {
    try {
      console.log('Fetching latest stock data from API...');
      const response = await fetch(`${API_BASE_URL}/api/latest`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Latest stock data received:', data);
      
      // Return in the format expected by React components
      return {
        id: data.id || 1,
        date: data.date,
        symbol: data.symbol,
        stockData: data.stockData,
        aiAnalysis: data.aiAnalysis
      };
    } catch (error) {
      console.error('Error fetching latest stock data:', error);
      // Return fallback data if API fails
      return this.getFallbackLatestData();
    }
  }

  async getHistoricalData(days = 30) {
    try {
      console.log('Fetching historical data from API...');
      const response = await fetch(`${API_BASE_URL}/api/historical`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Historical data received:', data.length, 'records');
      
      return data;
    } catch (error) {
      console.error('Error fetching historical data:', error);
      return this.getFallbackHistoricalData();
    }
  }

  async getAllRecommendations() {
    try {
      console.log('Fetching recommendations from API...');
      const response = await fetch(`${API_BASE_URL}/api/recommendations`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Recommendations received:', data.length, 'records');
      
      return data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      return this.getFallbackRecommendations();
    }
  }

  async getPerformanceMetrics() {
    try {
      console.log('Fetching performance metrics from API...');
      const response = await fetch(`${API_BASE_URL}/api/metrics`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Performance metrics received:', data);
      
      return data;
    } catch (error) {
      console.error('Error fetching performance metrics:', error);
      return this.getFallbackMetrics();
    }
  }

  // Fallback data methods (in case API is down)
  getFallbackLatestData() {
    return {
      id: 1,
      date: '2025-09-12',
      symbol: 'AAPL',
      stockData: {
        open: 229.22,
        close: 234.07,
        high: 234.51,
        low: 229.02,
        volume: 55824216,
        vwap: 231.5,
        transactions: 850000,
        change: 4.85,
        changePercent: 2.12
      },
      aiAnalysis: {
        sentiment: 'bullish',
        riskScore: 6,
        pricePrediction: 235.0,
        recommendations: [
          'Buy AAPL due to strong quarterly earnings',
          'AAPL is a good long-term investment opportunity',
          'The recent price increase is a buying signal'
        ],
        analysis: 'AAPL shows strong momentum, expect continued growth',
        model: 'meta-llama/llama-3.2-3b-instruct:free'
      }
    };
  }

  getFallbackHistoricalData() {
    return [
      { date: '2025-09-10', open: 232.185, close: 226.79, high: 232.42, low: 225.95, volume: 83440810, vwap: 229.6 },
      { date: '2025-09-11', open: 226.875, close: 230.03, high: 230.45, low: 226.65, volume: 50208578, vwap: 228.5 },
      { date: '2025-09-12', open: 229.22, close: 234.07, high: 234.51, low: 229.02, volume: 55824216, vwap: 231.5 }
    ];
  }

  getFallbackRecommendations() {
    return [
      {
        date: '2025-09-12',
        symbol: 'AAPL',
        sentiment: 'bullish',
        riskScore: 6,
        pricePrediction: 235.0,
        actualPrice: 234.07,
        recommendations: ['Buy AAPL due to strong quarterly earnings', 'Good long-term investment'],
        changePercent: 2.12,
        predictionAccuracy: 99.6
      }
    ];
  }

  getFallbackMetrics() {
    return {
      totalDaysAnalyzed: 7,
      totalRecommendations: 7,
      sentimentDistribution: { bullish: 4, bearish: 3 },
      averageRiskScore: 6.43,
      priceMetrics: {
        minPrice: 226.79,
        maxPrice: 234.07,
        avgPrice: 230.3,
        avgVolume: 63157868
      }
    };
  }
}

const databaseService = new DatabaseService();
export default databaseService;