import React from 'react';
import { Clock, X } from 'lucide-react';
import { Product } from '../types';
import ProductCard from './ProductCard';

interface RecentlyViewedProps {
  products: Product[];
  onProductClick: (product: Product) => void;
  onSellerClick: (sellerId: string) => void;
  onClearHistory: () => void;
}

const RecentlyViewed: React.FC<RecentlyViewedProps> = ({
  products,
  onProductClick,
  onSellerClick,
  onClearHistory
}) => {
  if (products.length === 0) return null;

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-3">
          <Clock className="h-6 w-6 text-gray-600" />
          <h2 className="text-2xl font-bold text-gray-900">Recently Viewed</h2>
        </div>
        <button
          onClick={onClearHistory}
          className="flex items-center space-x-2 text-gray-500 hover:text-red-600 transition-colors"
        >
          <X className="h-4 w-4" />
          <span className="text-sm">Clear History</span>
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.slice(0, 4).map(product => (
          <ProductCard
            key={product.id}
            product={product}
            onProductClick={onProductClick}
            onSellerClick={onSellerClick}
          />
        ))}
      </div>
    </section>
  );
};

export default RecentlyViewed;