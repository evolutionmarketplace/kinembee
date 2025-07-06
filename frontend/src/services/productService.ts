import { API_ENDPOINTS, apiRequest } from '../config/api';
import { Product } from '../types';

export interface CreateProductData {
  title: string;
  description: string;
  price: number;
  category: string;
  subcategory?: string;
  condition: 'new' | 'used' | 'refurbished';
  location?: string;
  images: File[];
}

export const productService = {
  // Get all products with filters
  getProducts: async (filters?: any): Promise<Product[]> => {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key] !== undefined && filters[key] !== '') {
          params.append(key, filters[key].toString());
        }
      });
    }

    const url = `${API_ENDPOINTS.PRODUCTS}${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await apiRequest(url);
    
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    
    const data = await response.json();
    return data.results || data;
  },

  // Get single product
  getProduct: async (id: string): Promise<Product> => {
    const response = await apiRequest(`${API_ENDPOINTS.PRODUCTS}${id}/`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch product');
    }
    
    return response.json();
  },

  // Create new product
  createProduct: async (productData: CreateProductData): Promise<Product> => {
    const formData = new FormData();
    
    // Add product data
    formData.append('title', productData.title);
    formData.append('description', productData.description);
    formData.append('price', productData.price.toString());
    formData.append('category', productData.category);
    formData.append('condition', productData.condition);
    
    if (productData.subcategory) {
      formData.append('subcategory', productData.subcategory);
    }
    
    if (productData.location) {
      formData.append('location', productData.location);
    }

    // Add images
    productData.images.forEach((image, index) => {
      formData.append(`uploaded_images`, image);
    });

    const response = await apiRequest(API_ENDPOINTS.PRODUCT_CREATE, {
      method: 'POST',
      headers: {
        // Don't set Content-Type for FormData, let browser set it
        'Authorization': `Bearer ${localStorage.getItem('evolutionMarketToken')}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create product');
    }

    return response.json();
  },

  // Update product
  updateProduct: async (id: string, productData: Partial<CreateProductData>): Promise<Product> => {
    const formData = new FormData();
    
    Object.keys(productData).forEach(key => {
      if (key === 'images' && productData.images) {
        productData.images.forEach((image) => {
          formData.append('uploaded_images', image);
        });
      } else if (productData[key as keyof CreateProductData] !== undefined) {
        formData.append(key, productData[key as keyof CreateProductData] as string);
      }
    });

    const response = await apiRequest(`${API_ENDPOINTS.PRODUCTS}${id}/update/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('evolutionMarketToken')}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to update product');
    }

    return response.json();
  },

  // Delete product
  deleteProduct: async (id: string): Promise<void> => {
    const response = await apiRequest(`${API_ENDPOINTS.PRODUCTS}${id}/delete/`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete product');
    }
  },

  // Get user's products
  getMyProducts: async (): Promise<Product[]> => {
    const response = await apiRequest(API_ENDPOINTS.MY_PRODUCTS);
    
    if (!response.ok) {
      throw new Error('Failed to fetch your products');
    }
    
    const data = await response.json();
    return data.results || data;
  },

  // Get featured products
  getFeaturedProducts: async (): Promise<Product[]> => {
    const response = await apiRequest(API_ENDPOINTS.FEATURED_PRODUCTS);
    
    if (!response.ok) {
      throw new Error('Failed to fetch featured products');
    }
    
    const data = await response.json();
    return data.results || data;
  },

  // Get trending products
  getTrendingProducts: async (): Promise<Product[]> => {
    const response = await apiRequest(API_ENDPOINTS.TRENDING_PRODUCTS);
    
    if (!response.ok) {
      throw new Error('Failed to fetch trending products');
    }
    
    const data = await response.json();
    return data.results || data;
  },

  // Mark product as sold
  markAsSold: async (id: string, buyerEmail?: string): Promise<void> => {
    const response = await apiRequest(`${API_ENDPOINTS.PRODUCTS}${id}/sold/`, {
      method: 'POST',
      body: JSON.stringify({ buyer_email: buyerEmail }),
    });

    if (!response.ok) {
      throw new Error('Failed to mark product as sold');
    }
  },
};

export default productService;