import React, { useState, useEffect } from 'react';
import databaseService from './services/database';
import StockOverview from './components/StockOverview';
import AIAnalysis from './components/AIAnalysis';
import RecommendationsTable from './components/RecommendationsTable';
import PerformanceMetrics from './components/PerformanceMetrics';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [latestData, setLatestData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Fetch all dashboard data
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('Fetching dashboard data...');

      // Fetch all data in parallel for better performance
      const [latest, recs, performanceMetrics] = await Promise.all([
        databaseService.getLatestStockData(),
        databaseService.getAllRecommendations(),
        databaseService.getPerformanceMetrics()
      ]);

      setLatestData(latest);
      setRecommendations(recs);
      setMetrics(performanceMetrics);
      setLastUpdated(new Date());

      console.log('Dashboard data loaded successfully');
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError(`Failed to load data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Initial data load
  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Auto-refresh data every 5 minutes
  useEffect(() => {
    const interval = setInterval(fetchDashboardData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  // Manual refresh function
  const handleRefresh = () => {
    fetchDashboardData();
  };

  if (loading && !latestData) {
    return <LoadingSpinner />;
  }

  if (error && !latestData) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-6 max-w-md">
          <h2 className="text-red-400 text-xl font-semibold mb-2">Connection Error</h2>
          <p className="text-gray-300 mb-4">{error}</p>
          <button 
            onClick={handleRefresh}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-gray-700/50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-white">
                Fintech Intelligence Dashboard
              </h1>
              <p className="text-gray-300 mt-1">
                Real-time AI-powered stock analysis
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              {lastUpdated && (
                <span className="text-sm text-gray-400">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
              
              <button
                onClick={handleRefresh}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
              >
                <svg className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Dashboard Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Error Banner (if error occurred but we have cached data) */}
        {error && latestData && (
          <div className="bg-yellow-900/20 border border-yellow-500 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-yellow-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span className="text-yellow-300">Data refresh failed. Showing cached data.</span>
            </div>
          </div>
        )}

        {/* Stock Overview Section */}
        {latestData && (
          <StockOverview 
            data={latestData} 
            loading={loading}
          />
        )}

        {/* AI Analysis Panel - Now Full Width */}
        <div className="mt-8">
          <AIAnalysis 
            data={latestData?.aiAnalysis}
            stockData={latestData?.stockData}
            loading={loading}
          />
        </div>

        {/* Performance Metrics */}
        {metrics && (
          <div className="mt-8">
            <PerformanceMetrics 
              data={metrics}
              loading={loading}
            />
          </div>
        )}

        {/* Recommendations Table */}
        <div className="mt-8">
          <RecommendationsTable 
            data={recommendations}
            loading={loading}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-black/20 backdrop-blur-sm border-t border-gray-700/50 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex justify-between items-center text-gray-400 text-sm">
            <div>
              <p>Fintech Intelligence Pipeline • Built with React & AI</p>
              <p className="mt-1">Real-time data from Polygon.io • Analysis by LLaMA 3.2</p>
            </div>
            
            <div className="text-right">
              <p>Total Records: {metrics?.totalDaysAnalyzed || 0}</p>
              <p className="mt-1">
                System Status: 
                <span className="text-green-400 ml-1">
                  {latestData ? 'Online' : 'Offline'}
                </span>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;