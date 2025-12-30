import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

function PerformanceMetrics({ data, loading }) {
  if (loading || !data) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-600 rounded w-48 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-gray-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Check if data structure is valid
  if (!data || typeof data !== 'object') {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <h3 className="text-xl font-semibold text-white mb-4">System Performance Metrics</h3>
        <div className="text-center py-8">
          <p className="text-gray-400">Performance data not available</p>
        </div>
      </div>
    );
  }

  // Safely prepare sentiment data with fallbacks
  const sentimentData = data.sentimentDistribution && typeof data.sentimentDistribution === 'object' 
    ? Object.entries(data.sentimentDistribution).map(([key, value]) => ({
        name: key.charAt(0).toUpperCase() + key.slice(1),
        value: Number(value) || 0,
        color: key === 'bullish' ? '#10B981' : key === 'bearish' ? '#EF4444' : '#F59E0B'
      }))
    : [];

  // Safely prepare price metrics with fallbacks
  const priceMetrics = data.priceMetrics || {};
  const priceMetricsData = [
    { name: 'Min', value: Number(priceMetrics.minPrice) || 0, color: '#EF4444' },
    { name: 'Avg', value: Number(priceMetrics.avgPrice) || 0, color: '#8B5CF6' },
    { name: 'Max', value: Number(priceMetrics.maxPrice) || 0, color: '#10B981' }
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-600 rounded-lg p-3 shadow-xl">
          <p className="text-white font-medium">{payload[0].name}</p>
          <p className="text-gray-300">
            {payload[0].name === 'Min' || payload[0].name === 'Avg' || payload[0].name === 'Max' 
              ? `$${Number(payload[0].value).toFixed(2)}`
              : payload[0].value
            }
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white">System Performance Metrics</h3>
        <div className="text-sm text-gray-400">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {/* Total Days Analyzed */}
        <div className="bg-white/5 rounded-lg p-4 border border-white/10">
          <div className="flex items-center justify-between mb-2">
            <div className="p-2 bg-blue-600/20 rounded-lg">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {Number(data.totalDaysAnalyzed) || 0}
          </div>
          <div className="text-sm text-gray-400">Days Analyzed</div>
        </div>

        {/* Total Recommendations */}
        <div className="bg-white/5 rounded-lg p-4 border border-white/10">
          <div className="flex items-center justify-between mb-2">
            <div className="p-2 bg-purple-600/20 rounded-lg">
              <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {Number(data.totalRecommendations) || 0}
          </div>
          <div className="text-sm text-gray-400">AI Recommendations</div>
        </div>

        {/* Average Risk Score */}
        <div className="bg-white/5 rounded-lg p-4 border border-white/10">
          <div className="flex items-center justify-between mb-2">
            <div className="p-2 bg-yellow-600/20 rounded-lg">
              <svg className="w-5 h-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {Number(data.averageRiskScore).toFixed(1) || '0.0'}/10
          </div>
          <div className="text-sm text-gray-400">Avg Risk Score</div>
        </div>

        {/* Average Volume */}
        <div className="bg-white/5 rounded-lg p-4 border border-white/10">
          <div className="flex items-center justify-between mb-2">
            <div className="p-2 bg-green-600/20 rounded-lg">
              <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {((Number(priceMetrics.avgVolume) || 0) / 1000000).toFixed(1)}M
          </div>
          <div className="text-sm text-gray-400">Avg Volume</div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Distribution Pie Chart */}
        <div className="bg-white/5 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Sentiment Distribution</h4>
          {sentimentData.length > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
                    labelLine={false}
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              No sentiment data available
            </div>
          )}
          
          {/* Legend */}
          <div className="flex justify-center space-x-6 mt-4">
            {sentimentData.map((item, index) => (
              <div key={index} className="flex items-center">
                <div 
                  className="w-3 h-3 rounded-full mr-2" 
                  style={{ backgroundColor: item.color }}
                ></div>
                <span className="text-gray-300 text-sm">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Price Range Bar Chart */}
        <div className="bg-white/5 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Price Range Analysis</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priceMetricsData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <XAxis 
                  dataKey="name" 
                  stroke="#9CA3AF"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#9CA3AF"
                  fontSize={12}
                  tickFormatter={(value) => `$${Number(value).toFixed(0)}`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar 
                  dataKey="value" 
                  radius={[4, 4, 0, 0]}
                >
                  {priceMetricsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          {/* Price Summary */}
          <div className="grid grid-cols-3 gap-4 mt-4">
            <div className="text-center">
              <div className="text-red-400 text-lg font-bold">
                ${Number(priceMetrics.minPrice).toFixed(2) || '0.00'}
              </div>
              <div className="text-gray-400 text-xs">Minimum</div>
            </div>
            <div className="text-center">
              <div className="text-purple-400 text-lg font-bold">
                ${Number(priceMetrics.avgPrice).toFixed(2) || '0.00'}
              </div>
              <div className="text-gray-400 text-xs">Average</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 text-lg font-bold">
                ${Number(priceMetrics.maxPrice).toFixed(2) || '0.00'}
              </div>
              <div className="text-gray-400 text-xs">Maximum</div>
            </div>
          </div>
        </div>
      </div>

      {/* System Health Indicators */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-600/10 border border-green-600/30 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-400 rounded-full mr-3"></div>
            <div>
              <div className="text-green-400 font-medium">System Status</div>
              <div className="text-green-300 text-sm">Operational</div>
            </div>
          </div>
        </div>
        
        <div className="bg-blue-600/10 border border-blue-600/30 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-400 rounded-full mr-3"></div>
            <div>
              <div className="text-blue-400 font-medium">Data Quality</div>
              <div className="text-blue-300 text-sm">High Accuracy</div>
            </div>
          </div>
        </div>
        
        <div className="bg-purple-600/10 border border-purple-600/30 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-purple-400 rounded-full mr-3"></div>
            <div>
              <div className="text-purple-400 font-medium">AI Performance</div>
              <div className="text-purple-300 text-sm">Optimized</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PerformanceMetrics;