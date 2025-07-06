import React from 'react';
import { Search, TrendingUp, Clock } from 'lucide-react';

interface SearchSuggestionsProps {
  query: string;
  isVisible: boolean;
  onSuggestionClick: (suggestion: string) => void;
  onClose: () => void;
}

const SearchSuggestions: React.FC<SearchSuggestionsProps> = ({
  query,
  isVisible,
  onSuggestionClick,
  onClose
}) => {
  // Mock suggestions - in a real app, these would come from an API
  const trendingSearches = [
    'iPhone 15',
    'MacBook Pro',
    'Gaming Chair',
    'Web Development',
    'Mountain Bike'
  ];

  const recentSearches = [
    'Laptop',
    'Furniture',
    'Car'
  ];

  const filteredSuggestions = trendingSearches.filter(item =>
    item.toLowerCase().includes(query.toLowerCase())
  );

  if (!isVisible) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 z-40"
        onClick={onClose}
      />
      
      {/* Suggestions Panel */}
      <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-xl z-50 mt-1 max-h-80 overflow-y-auto">
        {query.length > 0 ? (
          <>
            {filteredSuggestions.length > 0 && (
              <div className="p-2">
                <div className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-500">
                  <Search className="h-4 w-4" />
                  <span>Suggestions</span>
                </div>
                {filteredSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => onSuggestionClick(suggestion)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-md transition-colors flex items-center space-x-3"
                  >
                    <Search className="h-4 w-4 text-gray-400" />
                    <span>{suggestion}</span>
                  </button>
                ))}
              </div>
            )}
          </>
        ) : (
          <>
            {/* Trending Searches */}
            <div className="p-2">
              <div className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-500">
                <TrendingUp className="h-4 w-4" />
                <span>Trending</span>
              </div>
              {trendingSearches.slice(0, 5).map((search, index) => (
                <button
                  key={index}
                  onClick={() => onSuggestionClick(search)}
                  className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-md transition-colors flex items-center space-x-3"
                >
                  <TrendingUp className="h-4 w-4 text-orange-500" />
                  <span>{search}</span>
                </button>
              ))}
            </div>

            {/* Recent Searches */}
            {recentSearches.length > 0 && (
              <div className="p-2 border-t border-gray-100">
                <div className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-500">
                  <Clock className="h-4 w-4" />
                  <span>Recent</span>
                </div>
                {recentSearches.map((search, index) => (
                  <button
                    key={index}
                    onClick={() => onSuggestionClick(search)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-md transition-colors flex items-center space-x-3"
                  >
                    <Clock className="h-4 w-4 text-gray-400" />
                    <span>{search}</span>
                  </button>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default SearchSuggestions;