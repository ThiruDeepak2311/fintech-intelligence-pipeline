import React from 'react';

function StockOverview({ data, loading }) {
  if (!data) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 animate-pulse">
            <div className="h-4 bg-gray-600 rounded mb-3"></div>
            <div className="h-8 bg-gray-600 rounded mb-2"></div>
            <div className="h-3 bg-gray-600 rounded w-2/3"></div>
          </div>
        ))}
      </div>
    );
  }

  const { stockData, symbol, date } = data;
  const isPositive = stockData.change >= 0;

  return (
    <div>
      {/* Main Stock Info Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 mb-6 text-white">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-4xl font-bold mb-2">{symbol}</h2>
            <p className="text-blue-100 text-lg">Apple Inc. • {date}</p>
          </div>
          
          <div className="mt-4 md:mt-0 text-right">
            <div className="text-5xl font-bold mb-2">
              ${stockData.close.toFixed(2)}
            </div>
            <div className={`flex items-center justify-end text-xl ${
              isPositive ? 'text-green-300' : 'text-red-300'
            }`}>
              <svg className={`w-6 h-6 mr-2 ${isPositive ? 'rotate-0' : 'rotate-180'}`} 
                   fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
              <span className="font-semibold">
                ${Math.abs(stockData.change).toFixed(2)} ({Math.abs(stockData.changePercent).toFixed(2)}%)
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Day Range */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-300 text-sm font-medium">Day Range</h3>
            <svg className="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-bold text-white">
              ${stockData.low} - ${stockData.high}
            </div>
            <div className="text-sm text-gray-400">
              Spread: ${(stockData.high - stockData.low).toFixed(2)}
            </div>
          </div>
        </div>

        {/* Volume */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-300 text-sm font-medium">Volume</h3>
            <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-bold text-white">
              {(stockData.volume / 1000000).toFixed(1)}M
            </div>
            <div className="text-sm text-gray-400">
              {stockData.volume.toLocaleString()} shares
            </div>
          </div>
        </div>

        {/* VWAP */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-300 text-sm font-medium">VWAP</h3>
            <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-bold text-white">
              ${stockData.vwap.toFixed(2)}
            </div>
            <div className={`text-sm ${
              stockData.close > stockData.vwap ? 'text-green-400' : 'text-red-400'
            }`}>
              {stockData.close > stockData.vwap ? 'Above' : 'Below'} VWAP
            </div>
          </div>
        </div>

        {/* Market Cap */}
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-300 text-sm font-medium">Est. Market Cap</h3>
            <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
            </svg>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-bold text-white">
              $3.6T
            </div>
            <div className="text-sm text-gray-400">
              15.2B shares outstanding
            </div>
          </div>
        </div>
      </div>

      {/* Today's Trading Summary */}
      <div className="mt-6 bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
        <h3 className="text-xl font-semibold text-white mb-4">Today's Trading Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <div className="text-sm text-gray-400 mb-1">Open</div>
            <div className="text-lg font-semibold text-white">${stockData.open.toFixed(2)}</div>
          </div>
          <div>
            <div className="text-sm text-gray-400 mb-1">High</div>
            <div className="text-lg font-semibold text-green-400">${stockData.high.toFixed(2)}</div>
          </div>
          <div>
            <div className="text-sm text-gray-400 mb-1">Low</div>
            <div className="text-lg font-semibold text-red-400">${stockData.low.toFixed(2)}</div>
          </div>
          <div>
            <div className="text-sm text-gray-400 mb-1">Close</div>
            <div className="text-lg font-semibold text-white">${stockData.close.toFixed(2)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StockOverview;