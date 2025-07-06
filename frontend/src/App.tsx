import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ProductCard from './components/ProductCard';
import CategoryCard from './components/CategoryCard';
import AuthModal from './components/AuthModal';
import ProductFilters from './components/ProductFilters';
import UserProfile from './components/UserProfile';
import ProductDetailModal from './components/ProductDetailModal';
import FloatingActionButton from './components/FloatingActionButton';
import QuickStats from './components/QuickStats';
import Toast from './components/Toast';
import AdvancedFilters from './components/AdvancedFilters';
import ProductComparison from './components/ProductComparison';
import SavedSearches from './components/SavedSearches';
import RecentlyViewed from './components/RecentlyViewed';
import SellProductModal from './components/SellProductModal';
import NotificationsModal from './components/NotificationsModal';
import { AuthProvider } from './context/AuthContext';
import { mockProducts, categories } from './data/mockData';
import { Product, Category, SearchFilters } from './types';
import { useToast } from './hooks/useToast';

function App() {
  const [currentView, setCurrentView] = useState<'home' | 'browse' | 'category'>('home');
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [isProductDetailOpen, setIsProductDetailOpen] = useState(false);
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [isAdvancedFiltersOpen, setIsAdvancedFiltersOpen] = useState(false);
  const [isComparisonOpen, setIsComparisonOpen] = useState(false);
  const [isSavedSearchesOpen, setIsSavedSearchesOpen] = useState(false);
  const [isSellModalOpen, setIsSellModalOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [compareProducts, setCompareProducts] = useState<Product[]>([]);
  const [recentlyViewed, setRecentlyViewed] = useState<Product[]>([]);
  const { toast, showToast, hideToast } = useToast();
  
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    category: '',
    minPrice: 0,
    maxPrice: 10000,
    condition: '',
    sortBy: 'date-desc',
    location: ''
  });

  // Simulate loading when changing views
  useEffect(() => {
    if (currentView !== 'home') {
      setIsLoading(true);
      const timer = setTimeout(() => setIsLoading(false), 800);
      return () => clearTimeout(timer);
    }
  }, [currentView, filters]);

  // Filter and search products
  const filteredProducts = mockProducts.filter(product => {
    const matchesQuery = !filters.query || 
      product.title.toLowerCase().includes(filters.query.toLowerCase()) ||
      product.description.toLowerCase().includes(filters.query.toLowerCase());
    
    const matchesCategory = !filters.category || product.category === filters.category;
    const matchesPrice = product.price >= filters.minPrice && product.price <= filters.maxPrice;
    const matchesCondition = !filters.condition || product.condition === filters.condition;
    const matchesLocation = !filters.location || 
      (product.location && product.location.toLowerCase().includes(filters.location.toLowerCase()));

    return matchesQuery && matchesCategory && matchesPrice && matchesCondition && matchesLocation;
  });

  // Sort products
  const sortedProducts = [...filteredProducts].sort((a, b) => {
    switch (filters.sortBy) {
      case 'price-asc':
        return a.price - b.price;
      case 'price-desc':
        return b.price - a.price;
      case 'popularity':
        return b.views - a.views;
      case 'date-desc':
      default:
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    }
  });

  const handleSearch = (query: string) => {
    setFilters(prev => ({ ...prev, query }));
    setCurrentView('browse');
    showToast(`Searching for "${query}"`, 'success');
  };

  const handleCategoryClick = (category: Category) => {
    setSelectedCategory(category);
    setFilters(prev => ({ ...prev, category: category.name }));
    setCurrentView('category');
    showToast(`Browsing ${category.name}`, 'success');
  };

  const handleProductClick = (product: Product) => {
    setSelectedProduct(product);
    setIsProductDetailOpen(true);
    
    // Add to recently viewed
    setRecentlyViewed(prev => {
      const filtered = prev.filter(p => p.id !== product.id);
      return [product, ...filtered].slice(0, 10);
    });
    
    // Simulate view increment
    product.views += 1;
  };

  const handleSellerClick = (sellerId: string) => {
    showToast('Seller profile feature coming soon!', 'warning');
  };

  const handleSellClick = () => {
    setIsSellModalOpen(true);
  };

  const handleProductCreated = () => {
    showToast('Product listed successfully! 🎉', 'success');
    // Refresh notifications
    window.dispatchEvent(new Event('storage'));
  };

  const handleAddToCompare = (product: Product) => {
    if (compareProducts.find(p => p.id === product.id)) {
      setCompareProducts(prev => prev.filter(p => p.id !== product.id));
      showToast('Removed from comparison', 'success');
    } else if (compareProducts.length >= 4) {
      showToast('Maximum 4 products can be compared', 'warning');
    } else {
      setCompareProducts(prev => [...prev, product]);
      showToast('Added to comparison', 'success');
    }
  };

  const handleRemoveFromCompare = (productId: string) => {
    setCompareProducts(prev => prev.filter(p => p.id !== productId));
  };

  const clearRecentlyViewed = () => {
    setRecentlyViewed([]);
    showToast('Recently viewed history cleared', 'success');
  };

  const featuredProducts = mockProducts.filter(product => product.isBoosted).slice(0, 6);
  const trendingProducts = mockProducts.sort((a, b) => b.views - a.views).slice(0, 8);

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Navbar
          onSearchChange={handleSearch}
          onAuthClick={() => setIsAuthModalOpen(true)}
          onProfileClick={() => setIsProfileModalOpen(true)}
          onNotificationsClick={() => setIsNotificationsOpen(true)}
          onSellClick={handleSellClick}
        />

        {currentView === 'home' && (
          <>
            <Hero onSearchChange={handleSearch} />
            
            {/* Quick Stats */}
            <QuickStats />
            
            {/* Categories Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Browse Categories</h2>
                <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                  Discover thousands of products and services across all categories
                </p>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-6">
                {categories.slice(0, 8).map(category => (
                  <CategoryCard
                    key={category.id}
                    category={category}
                    onCategoryClick={handleCategoryClick}
                  />
                ))}
              </div>
              
              <div className="text-center mt-8 space-x-4">
                <button
                  onClick={() => setCurrentView('browse')}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-medium transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  View All Products
                </button>
                <button
                  onClick={() => setIsSavedSearchesOpen(true)}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-8 py-3 rounded-full font-medium transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  Saved Searches
                </button>
              </div>
            </section>

            {/* Featured Products */}
            {featuredProducts.length > 0 && (
              <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 bg-white rounded-3xl mx-4 shadow-sm">
                <div className="text-center mb-12">
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured Listings</h2>
                  <p className="text-lg text-gray-600">
                    Premium listings from verified sellers
                  </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {featuredProducts.map(product => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      onProductClick={handleProductClick}
                      onSellerClick={handleSellerClick}
                      onAddToCompare={handleAddToCompare}
                      isInCompareList={compareProducts.some(p => p.id === product.id)}
                      showCompareButton={true}
                    />
                  ))}
                </div>
              </section>
            )}

            {/* Trending Products */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Trending Now</h2>
                <p className="text-lg text-gray-600">
                  Most viewed products this week
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {trendingProducts.map(product => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    onProductClick={handleProductClick}
                    onSellerClick={handleSellerClick}
                    onAddToCompare={handleAddToCompare}
                    isInCompareList={compareProducts.some(p => p.id === product.id)}
                    showCompareButton={true}
                  />
                ))}
              </div>
            </section>

            {/* Recently Viewed */}
            <RecentlyViewed
              products={recentlyViewed}
              onProductClick={handleProductClick}
              onSellerClick={handleSellerClick}
              onClearHistory={clearRecentlyViewed}
            />
          </>
        )}

        {(currentView === 'browse' || currentView === 'category') && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  {currentView === 'category' && selectedCategory
                    ? `${selectedCategory.name} Products`
                    : 'Browse All Products'
                  }
                </h1>
                <p className="text-gray-600">
                  {sortedProducts.length} products found
                  {filters.query && ` for "${filters.query}"`}
                </p>
              </div>
              
              <div className="flex items-center space-x-3">
                {compareProducts.length > 0 && (
                  <button
                    onClick={() => setIsComparisonOpen(true)}
                    className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <span>Compare ({compareProducts.length})</span>
                  </button>
                )}
                
                <button
                  onClick={() => setIsAdvancedFiltersOpen(true)}
                  className="flex items-center space-x-2 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <span>Advanced Filters</span>
                </button>
              </div>
            </div>

            <div className="flex flex-col lg:flex-row gap-8">
              {/* Filters Sidebar */}
              <div className="lg:w-80">
                <ProductFilters
                  filters={filters}
                  onFiltersChange={setFilters}
                  isOpen={isFiltersOpen}
                  onToggle={() => setIsFiltersOpen(!isFiltersOpen)}
                />
              </div>

              {/* Products Grid */}
              <div className="flex-1">
                {isLoading ? (
                  <div className="flex items-center justify-center py-20">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                      <p className="text-gray-600">Loading products...</p>
                    </div>
                  </div>
                ) : sortedProducts.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {sortedProducts.map(product => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        onProductClick={handleProductClick}
                        onSellerClick={handleSellerClick}
                        onAddToCompare={handleAddToCompare}
                        isInCompareList={compareProducts.some(p => p.id === product.id)}
                        showCompareButton={true}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-16">
                    <div className="h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                      <svg className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47.58-6.53 1.582" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-medium text-gray-900 mb-2">No products found</h3>
                    <p className="text-gray-500 mb-6">Try adjusting your search or filters</p>
                    <button
                      onClick={() => {
                        setFilters({
                          query: '',
                          category: '',
                          minPrice: 0,
                          maxPrice: 10000,
                          condition: '',
                          sortBy: 'date-desc',
                          location: ''
                        });
                      }}
                      className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Clear Filters
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Floating Action Button */}
        <FloatingActionButton onSellClick={handleSellClick} />

        {/* Modals */}
        <AuthModal
          isOpen={isAuthModalOpen}
          onClose={() => setIsAuthModalOpen(false)}
        />

        <UserProfile
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
          onSellClick={handleSellClick}
        />

        <ProductDetailModal
          product={selectedProduct}
          isOpen={isProductDetailOpen}
          onClose={() => setIsProductDetailOpen(false)}
          onSellerClick={handleSellerClick}
        />

        <AdvancedFilters
          filters={filters}
          onFiltersChange={setFilters}
          isOpen={isAdvancedFiltersOpen}
          onClose={() => setIsAdvancedFiltersOpen(false)}
        />

        <ProductComparison
          products={compareProducts}
          isOpen={isComparisonOpen}
          onClose={() => setIsComparisonOpen(false)}
          onRemoveProduct={handleRemoveFromCompare}
        />

        <SavedSearches
          isOpen={isSavedSearchesOpen}
          onClose={() => setIsSavedSearchesOpen(false)}
        />

        <SellProductModal
          isOpen={isSellModalOpen}
          onClose={() => setIsSellModalOpen(false)}
          onProductCreated={handleProductCreated}
        />

        <NotificationsModal
          isOpen={isNotificationsOpen}
          onClose={() => setIsNotificationsOpen(false)}
        />

        {/* Toast Notifications */}
        <Toast
          message={toast.message}
          type={toast.type}
          isVisible={toast.isVisible}
          onClose={hideToast}
        />

        {/* Footer */}
        <footer className="bg-gray-900 text-white mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="col-span-1 md:col-span-2">
                <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent mb-4">
                  Evolution Market
                </div>
                <p className="text-gray-400 mb-6 max-w-md">
                  Your trusted peer-to-peer marketplace for buying and selling everything. 
                  Connect with your community and discover amazing deals.
                </p>
                <div className="flex space-x-4">
                  <div className="h-10 w-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                    <span className="text-sm">f</span>
                  </div>
                  <div className="h-10 w-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                    <span className="text-sm">t</span>
                  </div>
                  <div className="h-10 w-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                    <span className="text-sm">i</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Quick Links</h4>
                <div className="space-y-2 text-gray-400">
                  <div className="hover:text-white transition-colors cursor-pointer">Browse Products</div>
                  <div 
                    onClick={handleSellClick}
                    className="hover:text-white transition-colors cursor-pointer"
                  >
                    Sell Item
                  </div>
                  <div className="hover:text-white transition-colors cursor-pointer">Categories</div>
                  <div className="hover:text-white transition-colors cursor-pointer">How it Works</div>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Support</h4>
                <div className="space-y-2 text-gray-400">
                  <div className="hover:text-white transition-colors cursor-pointer">Help Center</div>
                  <div className="hover:text-white transition-colors cursor-pointer">Contact Us</div>
                  <div className="hover:text-white transition-colors cursor-pointer">Safety Tips</div>
                  <div className="hover:text-white transition-colors cursor-pointer">Terms & Privacy</div>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-800 pt-8 mt-12 text-center text-gray-400">
              <p>&copy; 2024 Evolution Digital Market. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </AuthProvider>
  );
}

export default App;