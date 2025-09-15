import React from 'react';

function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center">
      <div className="text-center">
        {/* Animated spinner */}
        <div className="relative">
          <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
          <div className="w-12 h-12 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin absolute top-2 left-1/2 transform -translate-x-1/2"></div>
        </div>
        
        {/* Loading text */}
        <div className="mt-6">
          <h2 className="text-white text-xl font-semibold mb-2">
            Loading Fintech Intelligence
          </h2>
          <p className="text-gray-300">
            Connecting to database and fetching real-time data...
          </p>
        </div>
        
        {/* Progress dots */}
        <div className="flex justify-center space-x-2 mt-4">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
          <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;