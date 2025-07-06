import React from 'react';
import { Heart, Eye, Star, MapPin, Zap, Plus, BarChart3 } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onProductClick: (product: Product) => void;
  onSellerClick: (sellerId: string) => void;
  onAddToCompare?: (product: Product) => void;
  isInCompareList?: boolean;
  showCompareButton?: boolean;
}

const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  onProductClick, 
  onSellerClick,
  onAddToCompare,
  isInCompareList = false,
  showCompareButton = false
}) => {
  const [isLiked, setIsLiked] = React.useState(false);
  const [imageLoaded, setImageLoaded] = React.useState(false);

  const handleLikeClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsLiked(!isLiked);
  };

  const handleSellerClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onSellerClick(product.sellerId);
  };

  const handleCompareClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onAddToCompare) {
      onAddToCompare(product);
    }
  };

  return (
    <div 
      className="bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer group border border-gray-100 overflow-hidden transform hover:-translate-y-1"
      onClick={() => onProductClick(product)}
    >
      {/* Image Container */}
      <div className="relative aspect-square overflow-hidden bg-gray-100">
        {!imageLoaded && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}
        
        <img
          src={product.images[0]}
          alt={product.title}
          className={`w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setImageLoaded(true)}
        />
        
        {/* Overlay elements */}
        <div className="absolute top-3 left-3 flex flex-col space-y-2">
          {product.isBoosted && (
            <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 shadow-lg">
              <Zap className="h-3 w-3" />
              <span>Boosted</span>
            </div>
          )}
          
          <div className="bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium shadow-lg">
            {product.condition === 'new' ? 'New' : product.condition === 'used' ? 'Used' : 'Refurbished'}
          </div>
        </div>
        
        <div className="absolute top-3 right-3 flex flex-col space-y-2">
          <button
            onClick={handleLikeClick}
            className="p-2 rounded-full bg-white/90 hover:bg-white transition-colors shadow-lg group/heart"
          >
            <Heart 
              className={`h-4 w-4 transition-colors group-hover/heart:scale-110 transform ${
                isLiked ? 'fill-red-500 text-red-500' : 'text-gray-600 hover:text-red-500'
              }`} 
            />
          </button>
          
          {showCompareButton && (
            <button
              onClick={handleCompareClick}
              className={`p-2 rounded-full transition-colors shadow-lg ${
                isInCompareList 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white/90 hover:bg-white text-gray-600 hover:text-blue-600'
              }`}
              title={isInCompareList ? 'Remove from compare' : 'Add to compare'}
            >
              <BarChart3 className="h-4 w-4" />
            </button>
          )}
        </div>
        
        {/* View count */}
        <div className="absolute bottom-3 right-3 bg-black/70 text-white px-2 py-1 rounded-full text-xs flex items-center space-x-1">
          <Eye className="h-3 w-3" />
          <span>{product.views}</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Price */}
        <div className="mb-2">
          <span className="text-2xl font-bold text-gray-900">
            ${product.price.toLocaleString()}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
          {product.title}
        </h3>

        {/* Category and Location */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
          <span className="bg-gray-100 px-2 py-1 rounded-full text-xs">
            {product.category}
          </span>
          {product.location && (
            <div className="flex items-center space-x-1">
              <MapPin className="h-3 w-3" />
              <span className="truncate max-w-20">{product.location}</span>
            </div>
          )}
        </div>

        {/* Seller Info */}
        <div className="flex items-center justify-between mb-3">
          <button
            onClick={handleSellerClick}
            className="flex items-center space-x-2 hover:text-blue-600 transition-colors"
          >
            <div className="h-6 w-6 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
              {product.sellerName.charAt(0).toUpperCase()}
            </div>
            <span className="text-sm font-medium text-gray-700 truncate max-w-20">
              {product.sellerName}
            </span>
          </button>
          
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            <span className="text-sm font-medium text-gray-700">
              {product.sellerRating.toFixed(1)}
            </span>
          </div>
        </div>

        {/* Contact Button */}
        <button className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-2 px-4 rounded-lg font-medium transition-all duration-200 transform hover:scale-[1.02] shadow-sm hover:shadow-md">
          Contact Seller
        </button>
      </div>
    </div>
  );
};

export default ProductCard;