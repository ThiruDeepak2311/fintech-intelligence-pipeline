// Mock data service - simulates your real database data
class DatabaseService {
  constructor() {
    this.mockData = this.generateMockData();
  }

  generateMockData() {
    return {
      latest: {
        id: 7,
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
      },
      historical: [
        { date: '2025-09-10', open: 232.185, close: 226.79, high: 232.42, low: 225.95, volume: 83440810, vwap: 229.6 },
        { date: '2025-09-11', open: 226.875, close: 230.03, high: 230.45, low: 226.65, volume: 50208578, vwap: 228.5 },
        { date: '2025-09-12', open: 229.22, close: 234.07, high: 234.51, low: 229.02, volume: 55824216, vwap: 231.5 }
      ],
      recommendations: [
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
        },
        {
          date: '2025-09-11',
          symbol: 'AAPL',
          sentiment: 'bullish',
          riskScore: 6,
          pricePrediction: 225.5,
          actualPrice: 230.03,
          recommendations: ['Buy AAPL for long term growth', 'Hold for stable financials'],
          changePercent: 1.39,
          predictionAccuracy: 98.0
        }
      ],
      metrics: {
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
      }
    };
  }

  async getLatestStockData() {
    await new Promise(resolve => setTimeout(resolve, 500));
    return this.mockData.latest;
  }

  async getHistoricalData(days = 30) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return this.mockData.historical;
  }

  async getAllRecommendations() {
    await new Promise(resolve => setTimeout(resolve, 400));
    return this.mockData.recommendations;
  }

  async getPerformanceMetrics() {
    await new Promise(resolve => setTimeout(resolve, 200));
    return this.mockData.metrics;
  }
}

const databaseService = new DatabaseService();
export default databaseService;