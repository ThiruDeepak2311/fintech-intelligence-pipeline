import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

function PriceChart({ data, symbol, loading }) {
  if (loading || !data || data.length === 0) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="h-6 bg-gray-600 rounded w-32 mb-2"></div>
            <div className="h-4 bg-gray-600 rounded w-24"></div>
          </div>
        </div>
        <div className="h-80 bg-gray-700 rounded animate-pulse"></div>
      </div>
    );
  }

  // Format data for chart
  const chartData = data.map(item => ({
    ...item,
    formattedDate: new Date(item.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-900 border border-gray-600 rounded-lg p-4 shadow-xl">
          <p className="text-white font-semibold mb-2">{label}</p>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-300">Open:</span>
              <span className="text-white font-medium">${data.open.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">High:</span>
              <span className="text-green-400 font-medium">${data.high.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">Low:</span>
              <span className="text-red-400 font-medium">${data.low.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">Close:</span>
              <span className="text-white font-medium">${data.close.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">Volume:</span>
              <span className="text-blue-400 font-medium">{(data.volume / 1000000).toFixed(1)}M</span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  // Calculate price range for better visualization
  const prices = data.map(d => d.close);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice;
  const yAxisMin = Math.max(0, minPrice - priceRange * 0.1);
  const yAxisMax = maxPrice + priceRange * 0.1;

  // Determine if overall trend is positive
  const firstPrice = data[0]?.close || 0;
  const lastPrice = data[data.length - 1]?.close || 0;
  const isPositiveTrend = lastPrice >= firstPrice;

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
      {/* Chart Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-white mb-1">
            {symbol} Price Chart
          </h3>
          <p className="text-gray-300 text-sm">
            Last {data.length} trading days • Real-time data
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <div className="text-sm text-gray-400">Price Range</div>
            <div className="text-white font-medium">
              ${minPrice.toFixed(2)} - ${maxPrice.toFixed(2)}
            </div>
          </div>
          
          <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            isPositiveTrend 
              ? 'bg-green-600/20 text-green-400' 
              : 'bg-red-600/20 text-red-400'
          }`}>
            <svg className={`w-4 h-4 mr-1 ${isPositiveTrend ? 'rotate-0' : 'rotate-180'}`} 
                 fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
            {isPositiveTrend ? 'Uptrend' : 'Downtrend'}
          </div>
        </div>
      </div>

      {/* Price Chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <defs>
              <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={isPositiveTrend ? "#10B981" : "#EF4444"} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={isPositiveTrend ? "#10B981" : "#EF4444"} stopOpacity={0.05}/>
              </linearGradient>
            </defs>
            
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
            
            <XAxis 
              dataKey="formattedDate" 
              stroke="#9CA3AF"
              fontSize={12}
              tickLine={false}
            />
            
            <YAxis 
              domain={[yAxisMin, yAxisMax]}
              stroke="#9CA3AF"
              fontSize={12}
              tickLine={false}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            
            <Tooltip content={<CustomTooltip />} />
            
            <Area
              type="monotone"
              dataKey="close"
              stroke={isPositiveTrend ? "#10B981" : "#EF4444"}
              strokeWidth={2}
              fill="url(#priceGradient)"
            />
            
            <Line
              type="monotone"
              dataKey="vwap"
              stroke="#8B5CF6"
              strokeWidth={1}
              strokeDasharray="5 5"
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Legend */}
      <div className="flex items-center justify-center space-x-6 mt-4 pt-4 border-t border-white/10">
        <div className="flex items-center">
          <div className={`w-3 h-3 rounded-full mr-2 ${
            isPositiveTrend ? 'bg-green-400' : 'bg-red-400'
          }`}></div>
          <span className="text-gray-300 text-sm">Close Price</span>
        </div>
        
        <div className="flex items-center">
          <div className="w-3 h-0.5 bg-purple-400 mr-2" style={{borderStyle: 'dashed'}}></div>
          <span className="text-gray-300 text-sm">VWAP</span>
        </div>
        
        <div className="flex items-center">
          <svg className="w-4 h-4 text-blue-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-gray-300 text-sm">Hover for details</span>
        </div>
      </div>
    </div>
  );
}

export default PriceChart;