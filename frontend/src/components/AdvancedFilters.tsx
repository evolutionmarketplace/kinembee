import React, { useState } from 'react';
import { Filter, MapPin, DollarSign, Calendar, Star, X, ChevronDown } from 'lucide-react';
import { SearchFilters } from '../types';

interface AdvancedFiltersProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
  isOpen: boolean;
  onClose: () => void;
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({
  filters,
  onFiltersChange,
  isOpen,
  onClose
}) => {
  const [expandedSections, setExpandedSections] = useState<string[]>(['price', 'condition']);

  const toggleSection = (section: string) => {
    setExpandedSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-end sm:items-center justify-center p-4">
      <div className="bg-white rounded-t-3xl sm:rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Filter className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-bold text-gray-900">Advanced Filters</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Price Range */}
          <div className="border border-gray-200 rounded-xl p-4">
            <button
              onClick={() => toggleSection('price')}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <DollarSign className="h-5 w-5 text-green-600" />
                <span className="font-semibold text-gray-900">Price Range</span>
              </div>
              <ChevronDown className={`h-5 w-5 text-gray-400 transition-transform ${
                expandedSections.includes('price') ? 'rotate-180' : ''
              }`} />
            </button>
            
            {expandedSections.includes('price') && (
              <div className="mt-4 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Minimum Price
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={filters.minPrice}
                      onChange={(e) => handleFilterChange('minPrice', parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="$0"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Maximum Price
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={filters.maxPrice}
                      onChange={(e) => handleFilterChange('maxPrice', parseInt(e.target.value) || 10000)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="$10,000"
                    />
                  </div>
                </div>
                
                {/* Quick Price Ranges */}
                <div className="flex flex-wrap gap-2">
                  {[
                    { label: 'Under $50', min: 0, max: 50 },
                    { label: '$50-$200', min: 50, max: 200 },
                    { label: '$200-$500', min: 200, max: 500 },
                    { label: '$500+', min: 500, max: 10000 }
                  ].map((range, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        handleFilterChange('minPrice', range.min);
                        handleFilterChange('maxPrice', range.max);
                      }}
                      className="px-3 py-1 text-sm bg-gray-100 hover:bg-blue-100 hover:text-blue-700 rounded-full transition-colors"
                    >
                      {range.label}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Location */}
          <div className="border border-gray-200 rounded-xl p-4">
            <button
              onClick={() => toggleSection('location')}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-red-600" />
                <span className="font-semibold text-gray-900">Location</span>
              </div>
              <ChevronDown className={`h-5 w-5 text-gray-400 transition-transform ${
                expandedSections.includes('location') ? 'rotate-180' : ''
              }`} />
            </button>
            
            {expandedSections.includes('location') && (
              <div className="mt-4 space-y-4">
                <input
                  type="text"
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter city, state, or zip code"
                />
                
                {/* Popular Locations */}
                <div className="flex flex-wrap gap-2">
                  {['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ'].map((city, index) => (
                    <button
                      key={index}
                      onClick={() => handleFilterChange('location', city)}
                      className="px-3 py-1 text-sm bg-gray-100 hover:bg-blue-100 hover:text-blue-700 rounded-full transition-colors"
                    >
                      {city}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Condition */}
          <div className="border border-gray-200 rounded-xl p-4">
            <button
              onClick={() => toggleSection('condition')}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <Star className="h-5 w-5 text-yellow-600" />
                <span className="font-semibold text-gray-900">Condition</span>
              </div>
              <ChevronDown className={`h-5 w-5 text-gray-400 transition-transform ${
                expandedSections.includes('condition') ? 'rotate-180' : ''
              }`} />
            </button>
            
            {expandedSections.includes('condition') && (
              <div className="mt-4 grid grid-cols-2 gap-3">
                {[
                  { value: '', label: 'Any Condition', color: 'bg-gray-100' },
                  { value: 'new', label: 'New', color: 'bg-green-100 text-green-800' },
                  { value: 'used', label: 'Used', color: 'bg-yellow-100 text-yellow-800' },
                  { value: 'refurbished', label: 'Refurbished', color: 'bg-blue-100 text-blue-800' }
                ].map((condition) => (
                  <button
                    key={condition.value}
                    onClick={() => handleFilterChange('condition', condition.value)}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      filters.condition === condition.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${condition.color}`}>
                      {condition.label}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Date Posted */}
          <div className="border border-gray-200 rounded-xl p-4">
            <button
              onClick={() => toggleSection('date')}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <Calendar className="h-5 w-5 text-purple-600" />
                <span className="font-semibold text-gray-900">Date Posted</span>
              </div>
              <ChevronDown className={`h-5 w-5 text-gray-400 transition-transform ${
                expandedSections.includes('date') ? 'rotate-180' : ''
              }`} />
            </button>
            
            {expandedSections.includes('date') && (
              <div className="mt-4 grid grid-cols-2 gap-3">
                {[
                  { label: 'Today', days: 1 },
                  { label: 'This Week', days: 7 },
                  { label: 'This Month', days: 30 },
                  { label: 'All Time', days: 0 }
                ].map((period, index) => (
                  <button
                    key={index}
                    className="p-3 text-sm border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                  >
                    {period.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="sticky bottom-0 bg-white border-t border-gray-100 p-6 flex space-x-3">
          <button
            onClick={() => {
              onFiltersChange({
                query: filters.query,
                category: '',
                minPrice: 0,
                maxPrice: 10000,
                condition: '',
                sortBy: 'date-desc',
                location: ''
              });
            }}
            className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-colors"
          >
            Clear All
          </button>
          <button
            onClick={onClose}
            className="flex-1 px-4 py-3 bg-gradient-to-r from-blue-600 to-emerald-600 text-white rounded-xl font-medium hover:from-blue-700 hover:to-emerald-700 transition-all transform hover:scale-[1.02]"
          >
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdvancedFilters;