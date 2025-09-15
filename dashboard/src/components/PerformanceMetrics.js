import React, { useState } from 'react';

function RecommendationsTable({ data, loading }) {
  const [sortField, setSortField] = useState('date');
  const [sortDirection, setSortDirection] = useState('desc');
  const [filterSentiment, setFilterSentiment] = useState('all');

  if (loading) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-600 rounded w-48 mb-6"></div>
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <h3 className="text-xl font-semibold text-white mb-4">AI Recommendations</h3>
        <div className="text-center py-12">
          <svg className="w-12 h-12 text-gray-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="text-gray-400">No recommendations available</p>
        </div>
      </div>
    );
  }

  // Filter and sort data
  const filteredData = data.filter(item => {
    if (filterSentiment === 'all') return true;
    return item.sentiment.toLowerCase() === filterSentiment;
  });

  const sortedData = [...filteredData].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];
    
    if (sortField === 'date') {
      aVal = new Date(aVal);
      bVal = new Date(bVal);
    }
    
    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const getSentimentBadge = (sentiment) => {
    const classes = {
      bullish: 'bg-green-600/20 text-green-400 border-green-600/30',
      bearish: 'bg-red-600/20 text-red-400 border-red-600/30',
      neutral: 'bg-yellow-600/20 text-yellow-400 border-yellow-600/30'
    };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold border capitalize ${classes[sentiment.toLowerCase()] || classes.neutral}`}>
        {sentiment}
      </span>
    );
  };

  const getRiskBadge = (score) => {
    let color = 'bg-green-600/20 text-green-400 border-green-600/30';
    let label = 'Low';
    
    if (score > 6) {
      color = 'bg-red-600/20 text-red-400 border-red-600/30';
      label = 'High';
    } else if (score > 3) {
      color = 'bg-yellow-600/20 text-yellow-400 border-yellow-600/30';
      label = 'Medium';
    }
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold border ${color}`}>
        {label} ({score}/10)
      </span>
    );
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
      {/* Header with filters */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h3 className="text-xl font-semibold text-white mb-4 md:mb-0">
          AI Recommendations History
        </h3>
        
        <div className="flex items-center space-x-4">
          <select
            value={filterSentiment}
            onChange={(e) => setFilterSentiment(e.target.value)}
            className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Sentiments</option>
            <option value="bullish">Bullish</option>
            <option value="bearish">Bearish</option>
            <option value="neutral">Neutral</option>
          </select>
          
          <span className="text-gray-400 text-sm">
            {sortedData.length} recommendations
          </span>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th 
                onClick={() => handleSort('date')}
                className="text-left py-3 px-2 text-gray-300 font-medium cursor-pointer hover:text-white transition-colors"
              >
                <div className="flex items-center">
                  Date
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                </div>
              </th>
              <th 
                onClick={() => handleSort('sentiment')}
                className="text-left py-3 px-2 text-gray-300 font-medium cursor-pointer hover:text-white transition-colors"
              >
                <div className="flex items-center">
                  Sentiment
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                </div>
              </th>
              <th 
                onClick={() => handleSort('riskScore')}
                className="text-left py-3 px-2 text-gray-300 font-medium cursor-pointer hover:text-white transition-colors"
              >
                <div className="flex items-center">
                  Risk
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                </div>
              </th>
              <th className="text-left py-3 px-2 text-gray-300 font-medium">
                Price Target
              </th>
              <th className="text-left py-3 px-2 text-gray-300 font-medium">
                Accuracy
              </th>
              <th className="text-left py-3 px-2 text-gray-300 font-medium">
                Performance
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((item, index) => (
              <tr key={index} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="py-4 px-2">
                  <div className="text-white font-medium">
                    {new Date(item.date).toLocaleDateString('en-US', { 
                      month: 'short', 
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </div>
                </td>
                
                <td className="py-4 px-2">
                  {getSentimentBadge(item.sentiment)}
                </td>
                
                <td className="py-4 px-2">
                  {getRiskBadge(item.riskScore)}
                </td>
                
                <td className="py-4 px-2">
                  <div className="text-white font-medium">
                    ${item.pricePrediction?.toFixed(2)}
                  </div>
                  <div className="text-gray-400 text-sm">
                    Actual: ${item.actualPrice?.toFixed(2)}
                  </div>
                </td>
                
                <td className="py-4 px-2">
                  <div className={`text-sm font-medium ${
                    item.predictionAccuracy >= 95 ? 'text-green-400' :
                    item.predictionAccuracy >= 90 ? 'text-yellow-400' : 'text-red-400'
                  }`}>
                    {item.predictionAccuracy?.toFixed(1)}%
                  </div>
                </td>
                
                <td className="py-4 px-2">
                  <div className={`text-sm font-medium flex items-center ${
                    item.changePercent >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    <svg className={`w-4 h-4 mr-1 ${item.changePercent >= 0 ? 'rotate-0' : 'rotate-180'}`} 
                         fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                    {Math.abs(item.changePercent).toFixed(2)}%
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recommendations Preview */}
      {sortedData.length > 0 && (
        <div className="mt-6 p-4 bg-white/5 rounded-lg">
          <h4 className="text-white font-medium mb-3">Latest Recommendations:</h4>
          <div className="space-y-2">
            {sortedData[0].recommendations?.slice(0, 2).map((rec, index) => (
              <div key={index} className="flex items-start text-sm">
                <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <span className="text-gray-300">{rec}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default RecommendationsTable;