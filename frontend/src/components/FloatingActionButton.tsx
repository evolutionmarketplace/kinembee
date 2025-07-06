import React, { useState } from 'react';
import { Plus, Package, Briefcase, X } from 'lucide-react';

interface FloatingActionButtonProps {
  onSellClick: () => void;
}

const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({ onSellClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="fixed bottom-6 right-6 z-40">
      {/* Expanded Options */}
      {isExpanded && (
        <div className="absolute bottom-16 right-0 space-y-3 animate-in slide-in-from-bottom-2 duration-200">
          <button
            onClick={() => {
              onSellClick();
              setIsExpanded(false);
            }}
            className="flex items-center space-x-3 bg-white hover:bg-gray-50 text-gray-700 px-4 py-3 rounded-full shadow-lg border border-gray-200 transition-all duration-200 transform hover:scale-105"
          >
            <Package className="h-5 w-5 text-blue-600" />
            <span className="font-medium">Sell Product</span>
          </button>
          
          <button
            onClick={() => {
              onSellClick();
              setIsExpanded(false);
            }}
            className="flex items-center space-x-3 bg-white hover:bg-gray-50 text-gray-700 px-4 py-3 rounded-full shadow-lg border border-gray-200 transition-all duration-200 transform hover:scale-105"
          >
            <Briefcase className="h-5 w-5 text-emerald-600" />
            <span className="font-medium">Offer Service</span>
          </button>
        </div>
      )}

      {/* Main FAB */}
      <button
        onClick={toggleExpanded}
        className={`h-14 w-14 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-700 hover:to-emerald-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-110 flex items-center justify-center ${
          isExpanded ? 'rotate-45' : ''
        }`}
      >
        {isExpanded ? (
          <X className="h-6 w-6" />
        ) : (
          <Plus className="h-6 w-6" />
        )}
      </button>
    </div>
  );
};

export default FloatingActionButton;