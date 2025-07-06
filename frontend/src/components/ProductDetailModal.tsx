import React, { useState } from 'react';
import { X, Heart, Share2, MapPin, Star, Phone, MessageCircle, Eye, Calendar, Shield, Zap } from 'lucide-react';
import { Product } from '../types';

interface ProductDetailModalProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onSellerClick: (sellerId: string) => void;
}

const ProductDetailModal: React.FC<ProductDetailModalProps> = ({ 
  product, 
  isOpen, 
  onClose, 
  onSellerClick 
}) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const [showContactInfo, setShowContactInfo] = useState(false);

  if (!isOpen || !product) return null;

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: product.title,
          text: product.description,
          url: window.location.href,
        });
      } catch (err) {
        console.log('Error sharing:', err);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      // You could show a toast notification here
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-4 flex items-center justify-between z-10">
          <h2 className="text-xl font-bold text-gray-900 truncate pr-4">
            {product.title}
          </h2>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsLiked(!isLiked)}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            >
              <Heart 
                className={`h-5 w-5 transition-colors ${
                  isLiked ? 'fill-red-500 text-red-500' : 'text-gray-600 hover:text-red-500'
                }`} 
              />
            </button>
            <button
              onClick={handleShare}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            >
              <Share2 className="h-5 w-5 text-gray-600 hover:text-blue-600" />
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            >
              <X className="h-5 w-5 text-gray-600" />
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 p-6">
          {/* Image Gallery */}
          <div className="space-y-4">
            <div className="relative aspect-square bg-gray-100 rounded-xl overflow-hidden">
              <img
                src={product.images[currentImageIndex]}
                alt={product.title}
                className="w-full h-full object-cover"
              />
              
              {product.isBoosted && (
                <div className="absolute top-4 left-4 bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1 shadow-lg">
                  <Zap className="h-4 w-4" />
                  <span>Boosted</span>
                </div>
              )}
              
              <div className="absolute bottom-4 right-4 bg-black/70 text-white px-3 py-1 rounded-full text-sm flex items-center space-x-1">
                <Eye className="h-4 w-4" />
                <span>{product.views} views</span>
              </div>
            </div>
            
            {product.images.length > 1 && (
              <div className="flex space-x-2 overflow-x-auto pb-2">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentImageIndex(index)}
                    className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${
                      currentImageIndex === index 
                        ? 'border-blue-500 ring-2 ring-blue-200' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <img
                      src={image}
                      alt={`${product.title} ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            {/* Price and Status */}
            <div className="flex items-center justify-between">
              <div>
                <div className="text-3xl font-bold text-gray-900">
                  ${product.price.toLocaleString()}
                </div>
                <div className="flex items-center space-x-2 mt-1">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    product.condition === 'new' 
                      ? 'bg-green-100 text-green-800' 
                      : product.condition === 'used'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {product.condition.charAt(0).toUpperCase() + product.condition.slice(1)}
                  </span>
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                    {product.category}
                  </span>
                </div>
              </div>
            </div>

            {/* Description */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-700 leading-relaxed">
                {product.description}
              </p>
            </div>

            {/* Location and Date */}
            <div className="grid grid-cols-2 gap-4 py-4 border-t border-gray-100">
              {product.location && (
                <div className="flex items-center space-x-2 text-gray-600">
                  <MapPin className="h-4 w-4" />
                  <span className="text-sm">{product.location}</span>
                </div>
              )}
              <div className="flex items-center space-x-2 text-gray-600">
                <Calendar className="h-4 w-4" />
                <span className="text-sm">Listed {formatDate(product.createdAt)}</span>
              </div>
            </div>

            {/* Seller Info */}
            <div className="bg-gray-50 rounded-xl p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Seller Information</h3>
              <div className="flex items-center justify-between">
                <button
                  onClick={() => onSellerClick(product.sellerId)}
                  className="flex items-center space-x-3 hover:bg-gray-100 rounded-lg p-2 transition-colors"
                >
                  <div className="h-12 w-12 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-lg font-bold">
                    {product.sellerName.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900 flex items-center space-x-1">
                      <span>{product.sellerName}</span>
                      <Shield className="h-4 w-4 text-green-500" />
                    </div>
                    <div className="flex items-center space-x-1 text-sm text-gray-600">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span>{product.sellerRating.toFixed(1)} rating</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            {/* Contact Actions */}
            <div className="space-y-3">
              {!showContactInfo ? (
                <button
                  onClick={() => setShowContactInfo(true)}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-3 px-6 rounded-xl font-semibold transition-all duration-200 transform hover:scale-[1.02] shadow-lg hover:shadow-xl"
                >
                  Show Contact Information
                </button>
              ) : (
                <div className="space-y-3">
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                    <div className="flex items-center space-x-2 text-blue-800 mb-2">
                      <Phone className="h-5 w-5" />
                      <span className="font-medium">Contact Seller</span>
                    </div>
                    <div className="text-blue-700">
                      <a 
                        href={`tel:${product.sellerContact}`}
                        className="text-lg font-semibold hover:underline"
                      >
                        {product.sellerContact}
                      </a>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-3">
                    <a
                      href={`tel:${product.sellerContact}`}
                      className="flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-xl font-medium transition-colors"
                    >
                      <Phone className="h-5 w-5" />
                      <span>Call</span>
                    </a>
                    <a
                      href={`https://wa.me/${product.sellerContact.replace(/[^\d]/g, '')}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center space-x-2 bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-xl font-medium transition-colors"
                    >
                      <MessageCircle className="h-5 w-5" />
                      <span>WhatsApp</span>
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Safety Tips */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
              <div className="flex items-start space-x-2">
                <Shield className="h-5 w-5 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800 mb-1">Safety Tips</h4>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    <li>• Meet in a public place for transactions</li>
                    <li>• Inspect items before payment</li>
                    <li>• Use secure payment methods</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailModal;