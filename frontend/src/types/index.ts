export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  isVerified: boolean;
  isAdmin: boolean;
  contactNumber?: string;
  createdAt: string;
}

export interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  images: string[];
  category: string;
  subcategory?: string;
  condition: 'new' | 'used' | 'refurbished';
  sellerId: string;
  sellerName: string;
  sellerContact: string;
  sellerRating: number;
  isBoosted: boolean;
  isActive: boolean;
  views: number;
  likes: number;
  createdAt: string;
  updatedAt: string;
  location?: string;
}

export interface Review {
  id: string;
  productId: string;
  reviewerId: string;
  reviewerName: string;
  rating: number;
  comment: string;
  createdAt: string;
}

export interface Category {
  id: string;
  name: string;
  type: 'goods' | 'services';
  icon: string;
  subcategories?: string[];
}

export interface SearchFilters {
  query: string;
  category: string;
  minPrice: number;
  maxPrice: number;
  condition: string;
  sortBy: 'price-asc' | 'price-desc' | 'date-desc' | 'popularity';
  location: string;
}