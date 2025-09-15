import React from 'react';

function AIAnalysis({ data, stockData, loading }) {
  if (loading || !data) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-600 rounded w-32 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-600 rounded"></div>
            <div className="h-4 bg-gray-600 rounded w-3/4"></div>
            <div className="h-4 bg-gray-600 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'bullish': return 'text-green-400 bg-green-600/20';
      case 'bearish': return 'text-red-400 bg-red-600/20';
      case 'neutral': return 'text-yellow-400 bg-yellow-600/20';
      default: return 'text-gray-400 bg-gray-600/20';
    }
  };

  const getRiskColor = (score) => {
    if (score <= 3) return 'text-green-400 bg-green-600/20';
    if (score <= 6) return 'text-yellow-400 bg-yellow-600/20';
    return 'text-red-400 bg-red-600/20';
  };

  const getRiskLabel = (score) => {
    if (score <= 3) return 'Low Risk';
    if (score <= 6) return 'Medium Risk';
    return 'High Risk';
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white">AI Analysis</h3>
        <div className="flex items-center text-sm text-gray-400">
          <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          {data.model?.includes('llama') ? 'LLaMA 3.2' : 'AI Model'}
        </div>
      </div>

      {/* Sentiment Analysis */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <span className="text-gray-300 text-sm font-medium">Market Sentiment</span>
          <div className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${getSentimentColor(data.sentiment)}`}>
            {data.sentiment}
          </div>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex items-center">
            {data.sentiment?.toLowerCase() === 'bullish' && (
              <svg className="w-6 h-6 text-green-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            )}
            {data.sentiment?.toLowerCase() === 'bearish' && (
              <svg className="w-6 h-6 text-red-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
            {data.sentiment?.toLowerCase() === 'neutral' && (
              <svg className="w-6 h-6 text-yellow-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
              </svg>
            )}
            <div>
              <p className="text-white text-sm">
                AI detected <span className="font-semibold">{data.sentiment?.toLowerCase()}</span> market conditions
              </p>
              <p className="text-gray-400 text-xs mt-1">
                Based on price movement and volume analysis
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <span className="text-gray-300 text-sm font-medium">Risk Assessment</span>
          <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(data.riskScore)}`}>
            {getRiskLabel(data.riskScore)}
          </div>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-white text-2xl font-bold">{data.riskScore}/10</span>
            <div className="flex space-x-1">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => (
                <div
                  key={i}
                  className={`w-2 h-4 rounded-sm ${
                    i <= data.riskScore
                      ? data.riskScore <= 3
                        ? 'bg-green-400'
                        : data.riskScore <= 6
                        ? 'bg-yellow-400'
                        : 'bg-red-400'
                      : 'bg-gray-600'
                  }`}
                />
              ))}
            </div>
          </div>
          <p className="text-gray-400 text-xs">
            Risk score considers volatility, volume, and market conditions
          </p>
        </div>
      </div>

      {/* Price Prediction */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <span className="text-gray-300 text-sm font-medium">Price Target</span>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-white text-2xl font-bold">
                ${data.pricePrediction?.toFixed(2)}
              </div>
              <div className="text-gray-400 text-xs">AI Prediction</div>
            </div>
            
            {stockData && (
              <div className="text-right">
                <div className="text-gray-300 text-sm">
                  Current: ${stockData.close?.toFixed(2)}
                </div>
                <div className={`text-xs ${
                  data.pricePrediction > stockData.close ? 'text-green-400' : 'text-red-400'
                }`}>
                  {data.pricePrediction > stockData.close ? '↑' : '↓'} 
                  {Math.abs(((data.pricePrediction - stockData.close) / stockData.close) * 100).toFixed(1)}%
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="mb-6">
        <h4 className="text-gray-300 text-sm font-medium mb-3">AI Recommendations</h4>
        <div className="space-y-3">
          {data.recommendations?.map((rec, index) => (
            <div key={index} className="bg-white/5 rounded-lg p-3 border-l-2 border-blue-500">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3 mt-0.5">
                  <span className="text-white text-xs font-bold">{index + 1}</span>
                </div>
                <p className="text-gray-200 text-sm leading-relaxed">{rec}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Summary */}
      {data.analysis && (
        <div>
          <h4 className="text-gray-300 text-sm font-medium mb-3">Summary</h4>
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-gray-200 text-sm leading-relaxed">
              {data.analysis}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AIAnalysis;