import React, { useState } from 'react';
import { Search, Menu, X, User, Heart, ShoppingBag, Plus } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import SearchSuggestions from './SearchSuggestions';
import NotificationBadge from './NotificationBadge';

interface NavbarProps {
  onSearchChange: (query: string) => void;
  onAuthClick: () => void;
  onProfileClick: () => void;
  onNotificationsClick: () => void;
  onSellClick: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ 
  onSearchChange, 
  onAuthClick, 
  onProfileClick, 
  onNotificationsClick,
  onSellClick
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearchChange(searchQuery);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setSearchQuery(suggestion);
    onSearchChange(suggestion);
    setShowSuggestions(false);
  };

  const handleLogout = () => {
    logout();
    setIsMenuOpen(false);
  };

  const handleSellClick = () => {
    if (isAuthenticated) {
      onSellClick();
    } else {
      onAuthClick();
    }
  };

  return (
    <nav className="bg-white shadow-lg border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-emerald-500 bg-clip-text text-transparent">
              Evolution Market
            </div>
          </div>

          {/* Search Bar - Desktop */}
          <div className="hidden md:flex flex-1 max-w-2xl mx-8 relative">
            <form onSubmit={handleSearchSubmit} className="w-full">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search for products, services..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => setShowSuggestions(true)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 hover:bg-gray-100 transition-colors"
                />
              </div>
            </form>
            
            <SearchSuggestions
              query={searchQuery}
              isVisible={showSuggestions}
              onSuggestionClick={handleSuggestionClick}
              onClose={() => setShowSuggestions(false)}
            />
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <button 
                  onClick={handleSellClick}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full font-medium transition-colors flex items-center space-x-2 transform hover:scale-105"
                >
                  <Plus className="h-4 w-4" />
                  <span>Sell</span>
                </button>
                
                <div className="flex items-center space-x-4">
                  <button className="text-gray-600 hover:text-blue-600 transition-colors p-2 relative">
                    <Heart className="h-5 w-5" />
                    <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                      3
                    </span>
                  </button>
                  <button className="text-gray-600 hover:text-blue-600 transition-colors p-2 relative">
                    <ShoppingBag className="h-5 w-5" />
                    <span className="absolute -top-1 -right-1 h-4 w-4 bg-blue-500 text-white text-xs rounded-full flex items-center justify-center">
                      2
                    </span>
                  </button>
                  
                  <NotificationBadge onClick={onNotificationsClick} />
                  
                  <div className="relative group">
                    <button 
                      onClick={onProfileClick}
                      className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors"
                    >
                      {user?.avatar ? (
                        <img 
                          src={user.avatar} 
                          alt={user.name}
                          className="h-8 w-8 rounded-full object-cover border-2 border-gray-200"
                        />
                      ) : (
                        <div className="h-8 w-8 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-sm font-medium border-2 border-gray-200">
                          {user?.name.charAt(0).toUpperCase()}
                        </div>
                      )}
                      <span className="font-medium">{user?.name}</span>
                    </button>
                    
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                      <button 
                        onClick={onProfileClick}
                        className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        My Profile
                      </button>
                      <button 
                        onClick={onProfileClick}
                        className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        My Listings
                      </button>
                      <button 
                        onClick={onNotificationsClick}
                        className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        Notifications
                      </button>
                      <button 
                        onClick={onProfileClick}
                        className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        Settings
                      </button>
                      <hr className="my-2" />
                      <button 
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 transition-colors"
                      >
                        Sign Out
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <button
                onClick={onAuthClick}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full font-medium transition-all duration-200 transform hover:scale-105"
              >
                Sign In
              </button>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden pb-4 relative">
          <form onSubmit={handleSearchSubmit}>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search products, services..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setShowSuggestions(true)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
              />
            </div>
          </form>
          
          <SearchSuggestions
            query={searchQuery}
            isVisible={showSuggestions}
            onSuggestionClick={handleSuggestionClick}
            onClose={() => setShowSuggestions(false)}
          />
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white">
          <div className="px-4 pt-2 pb-4 space-y-2">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-3 py-3 border-b border-gray-100">
                  {user?.avatar ? (
                    <img 
                      src={user.avatar} 
                      alt={user.name}
                      className="h-10 w-10 rounded-full object-cover"
                    />
                  ) : (
                    <div className="h-10 w-10 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white font-medium">
                      {user?.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <div>
                    <div className="font-medium text-gray-900">{user?.name}</div>
                    <div className="text-sm text-gray-500">{user?.email}</div>
                  </div>
                </div>
                
                <button 
                  onClick={() => {
                    handleSellClick();
                    setIsMenuOpen(false);
                  }}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                >
                  <Plus className="h-5 w-5" />
                  <span>Sell Item</span>
                </button>
                
                <button 
                  onClick={() => {
                    onProfileClick();
                    setIsMenuOpen(false);
                  }}
                  className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors flex items-center space-x-3"
                >
                  <User className="h-5 w-5" />
                  <span>My Profile</span>
                </button>
                
                <button 
                  onClick={() => {
                    onNotificationsClick();
                    setIsMenuOpen(false);
                  }}
                  className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors flex items-center space-x-3"
                >
                  <NotificationBadge onClick={() => {}} />
                  <span>Notifications</span>
                </button>
                
                <button className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors flex items-center space-x-3">
                  <Heart className="h-5 w-5" />
                  <span>Favorites</span>
                  <span className="ml-auto bg-red-100 text-red-600 text-xs px-2 py-1 rounded-full">3</span>
                </button>
                
                <button className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors flex items-center space-x-3">
                  <ShoppingBag className="h-5 w-5" />
                  <span>My Cart</span>
                  <span className="ml-auto bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full">2</span>
                </button>
                
                <button 
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <button
                onClick={() => {
                  onAuthClick();
                  setIsMenuOpen(false);
                }}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-medium transition-colors"
              >
                Sign In / Register
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;