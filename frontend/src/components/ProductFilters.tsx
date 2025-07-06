import React from 'react';
import { Filter, X } from 'lucide-react';
import { categories } from '../data/mockData';
import { SearchFilters } from '../types';

interface ProductFiltersProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
  isOpen: boolean;
  onToggle: () => void;
}

const ProductFilters: React.FC<ProductFiltersProps> = ({
  filters,
  onFiltersChange,
  isOpen,
  onToggle
}) => {
  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  const clearFilters = () => {
    onFiltersChange({
      query: filters.query,
      category: '',
      minPrice: 0,
      maxPrice: 10000,
      condition: '',
      sortBy: 'date-desc',
      location: ''
    });
  };

  const hasActiveFilters = filters.category || filters.condition || filters.minPrice > 0 || filters.maxPrice < 10000 || filters.location;

  return (
    <>
      {/* Filter Toggle Button */}
      <button
        onClick={onToggle}
        className="lg:hidden flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <Filter className="h-5 w-5" />
        <span>Filters</span>
        {hasActiveFilters && (
          <div className="h-2 w-2 bg-blue-600 rounded-full"></div>
        )}
      </button>

      {/* Filter Panel */}
      <div className={`
        ${isOpen ? 'block' : 'hidden'} lg:block
        bg-white rounded-xl shadow-lg border border-gray-100 p-6 space-y-6
      `}>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>Filters</span>
          </h3>
          
          <div className="flex items-center space-x-2">
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
              >
                Clear All
              </button>
            )}
            <button
              onClick={onToggle}
              className="lg:hidden text-gray-400 hover:text-gray-600 p-1"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Category Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Category
          </label>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="category"
                value=""
                checked={filters.category === ''}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">All Categories</span>
            </label>
            {categories.map(category => (
              <label key={category.id} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="category"
                  value={category.name}
                  checked={filters.category === category.name}
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">{category.name}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Price Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Price Range
          </label>
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Min Price</label>
                <input
                  type="number"
                  min="0"
                  value={filters.minPrice}
                  onChange={(e) => handleFilterChange('minPrice', parseInt(e.target.value) || 0)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="$0"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Max Price</label>
                <input
                  type="number"
                  min="0"
                  value={filters.maxPrice}
                  onChange={(e) => handleFilterChange('maxPrice', parseInt(e.target.value) || 10000)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="$10,000"
                />
              </div>
            </div>
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>${filters.minPrice.toLocaleString()}</span>
              <span>${filters.maxPrice.toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* Condition Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Condition
          </label>
          <div className="space-y-2">
            {['', 'new', 'used', 'refurbished'].map(condition => (
              <label key={condition} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="condition"
                  value={condition}
                  checked={filters.condition === condition}
                  onChange={(e) => handleFilterChange('condition', e.target.value)}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">
                  {condition === '' ? 'Any Condition' : condition.charAt(0).toUpperCase() + condition.slice(1)}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Sort By */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Sort By
          </label>
          <select
            value={filters.sortBy}
            onChange={(e) => handleFilterChange('sortBy', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="date-desc">Newest First</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="popularity">Most Popular</option>
          </select>
        </div>

        {/* Location Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Location
          </label>
          <input
            type="text"
            value={filters.location}
            onChange={(e) => handleFilterChange('location', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            placeholder="Enter city or state"
          />
        </div>
      </div>
    </>
  );
};

export default ProductFilters;