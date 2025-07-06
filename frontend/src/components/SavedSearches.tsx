import React, { useState } from 'react';
import { Search, Bell, Trash2, Edit3, Plus, X } from 'lucide-react';

interface SavedSearch {
  id: string;
  name: string;
  query: string;
  filters: any;
  alertsEnabled: boolean;
  createdAt: string;
  resultCount: number;
}

interface SavedSearchesProps {
  isOpen: boolean;
  onClose: () => void;
}

const SavedSearches: React.FC<SavedSearchesProps> = ({ isOpen, onClose }) => {
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([
    {
      id: '1',
      name: 'iPhone 15 Pro',
      query: 'iPhone 15 Pro',
      filters: { category: 'Electronics', maxPrice: 1200 },
      alertsEnabled: true,
      createdAt: '2024-01-15T10:00:00Z',
      resultCount: 12
    },
    {
      id: '2',
      name: 'Gaming Laptops',
      query: 'gaming laptop',
      filters: { category: 'Electronics', minPrice: 800, maxPrice: 2000 },
      alertsEnabled: false,
      createdAt: '2024-01-10T15:30:00Z',
      resultCount: 8
    }
  ]);

  const [isCreating, setIsCreating] = useState(false);
  const [newSearchName, setNewSearchName] = useState('');

  if (!isOpen) return null;

  const toggleAlert = (id: string) => {
    setSavedSearches(prev =>
      prev.map(search =>
        search.id === id
          ? { ...search, alertsEnabled: !search.alertsEnabled }
          : search
      )
    );
  };

  const deleteSearch = (id: string) => {
    setSavedSearches(prev => prev.filter(search => search.id !== id));
  };

  const createNewSearch = () => {
    if (newSearchName.trim()) {
      const newSearch: SavedSearch = {
        id: Date.now().toString(),
        name: newSearchName,
        query: 'current search query', // This would come from current search state
        filters: {},
        alertsEnabled: true,
        createdAt: new Date().toISOString(),
        resultCount: 0
      };
      setSavedSearches(prev => [newSearch, ...prev]);
      setNewSearchName('');
      setIsCreating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Search className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-bold text-gray-900">Saved Searches</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <div className="p-6">
          {/* Create New Search */}
          <div className="mb-6">
            {isCreating ? (
              <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                <div className="flex items-center space-x-3 mb-3">
                  <Plus className="h-5 w-5 text-blue-600" />
                  <span className="font-medium text-blue-900">Save Current Search</span>
                </div>
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={newSearchName}
                    onChange={(e) => setNewSearchName(e.target.value)}
                    placeholder="Enter search name..."
                    className="flex-1 px-3 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    autoFocus
                  />
                  <button
                    onClick={createNewSearch}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Save
                  </button>
                  <button
                    onClick={() => setIsCreating(false)}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => setIsCreating(true)}
                className="w-full flex items-center justify-center space-x-2 p-4 border-2 border-dashed border-gray-300 rounded-xl hover:border-blue-400 hover:bg-blue-50 transition-colors"
              >
                <Plus className="h-5 w-5 text-gray-400" />
                <span className="text-gray-600 font-medium">Save Current Search</span>
              </button>
            )}
          </div>

          {/* Saved Searches List */}
          <div className="space-y-4">
            {savedSearches.length > 0 ? (
              savedSearches.map((search) => (
                <div
                  key={search.id}
                  className="bg-gray-50 border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <h3 className="font-semibold text-gray-900">{search.name}</h3>
                        {search.alertsEnabled && (
                          <div className="flex items-center space-x-1 bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">
                            <Bell className="h-3 w-3" />
                            <span>Alerts On</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-sm text-gray-600 mb-2">
                        Query: "{search.query}"
                      </div>
                      
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{search.resultCount} results</span>
                        <span>Created {new Date(search.createdAt).toLocaleDateString()}</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => toggleAlert(search.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          search.alertsEnabled
                            ? 'bg-green-100 text-green-600 hover:bg-green-200'
                            : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                        }`}
                        title={search.alertsEnabled ? 'Disable alerts' : 'Enable alerts'}
                      >
                        <Bell className="h-4 w-4" />
                      </button>
                      
                      <button
                        className="p-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-colors"
                        title="Edit search"
                      >
                        <Edit3 className="h-4 w-4" />
                      </button>
                      
                      <button
                        onClick={() => deleteSearch(search.id)}
                        className="p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
                        title="Delete search"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                      Run Search
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-12">
                <Search className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No saved searches</h3>
                <p className="text-gray-500">Save your searches to get notified of new listings</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SavedSearches;