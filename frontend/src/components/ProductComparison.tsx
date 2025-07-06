import React, { useState } from 'react';
import { X, Plus, Minus, Star, MapPin, Calendar, Eye } from 'lucide-react';
import { Product } from '../types';

interface ProductComparisonProps {
  products: Product[];
  isOpen: boolean;
  onClose: () => void;
  onRemoveProduct: (productId: string) => void;
}

const ProductComparison: React.FC<ProductComparisonProps> = ({
  products,
  isOpen,
  onClose,
  onRemoveProduct
}) => {
  if (!isOpen || products.length === 0) return null;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            Compare Products ({products.length})
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-6 w-6 text-gray-500" />
          </button>
        </div>

        {/* Comparison Table */}
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr>
                  <td className="w-48 p-4 font-semibold text-gray-900 border-b border-gray-200">
                    Product
                  </td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4 border-b border-gray-200 min-w-64">
                      <div className="relative">
                        <button
                          onClick={() => onRemoveProduct(product.id)}
                          className="absolute -top-2 -right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors z-10"
                        >
                          <X className="h-3 w-3" />
                        </button>
                        <img
                          src={product.images[0]}
                          alt={product.title}
                          className="w-full h-32 object-cover rounded-lg mb-3"
                        />
                        <h3 className="font-semibold text-gray-900 text-sm line-clamp-2">
                          {product.title}
                        </h3>
                      </div>
                    </td>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {/* Price */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Price</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <span className="text-2xl font-bold text-green-600">
                        ${product.price.toLocaleString()}
                      </span>
                    </td>
                  ))}
                </tr>

                {/* Condition */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Condition</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        product.condition === 'new' 
                          ? 'bg-green-100 text-green-800' 
                          : product.condition === 'used'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {product.condition.charAt(0).toUpperCase() + product.condition.slice(1)}
                      </span>
                    </td>
                  ))}
                </tr>

                {/* Category */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Category</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <span className="text-gray-600">{product.category}</span>
                    </td>
                  ))}
                </tr>

                {/* Seller */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Seller</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <div className="flex items-center space-x-2">
                        <div className="h-8 w-8 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                          {product.sellerName.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <div className="font-medium text-gray-900 text-sm">
                            {product.sellerName}
                          </div>
                          <div className="flex items-center space-x-1 text-xs text-gray-500">
                            <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                            <span>{product.sellerRating.toFixed(1)}</span>
                          </div>
                        </div>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Location */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Location</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      {product.location ? (
                        <div className="flex items-center space-x-1 text-gray-600">
                          <MapPin className="h-4 w-4" />
                          <span className="text-sm">{product.location}</span>
                        </div>
                      ) : (
                        <span className="text-gray-400 text-sm">Not specified</span>
                      )}
                    </td>
                  ))}
                </tr>

                {/* Views */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Views</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <div className="flex items-center space-x-1 text-gray-600">
                        <Eye className="h-4 w-4" />
                        <span className="text-sm">{product.views}</span>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Date Listed */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Listed</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <div className="flex items-center space-x-1 text-gray-600">
                        <Calendar className="h-4 w-4" />
                        <span className="text-sm">{formatDate(product.createdAt)}</span>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Actions */}
                <tr>
                  <td className="p-4 font-medium text-gray-700">Actions</td>
                  {products.map((product) => (
                    <td key={product.id} className="p-4">
                      <div className="space-y-2">
                        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded-lg text-sm font-medium transition-colors">
                          View Details
                        </button>
                        <button className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-3 rounded-lg text-sm font-medium transition-colors">
                          Contact Seller
                        </button>
                      </div>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductComparison;