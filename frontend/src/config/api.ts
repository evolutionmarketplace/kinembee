// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend.railway.app';

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: `${API_BASE_URL}/api/v1/auth/login/`,
  REGISTER: `${API_BASE_URL}/api/v1/auth/register/`,
  LOGOUT: `${API_BASE_URL}/api/v1/auth/logout/`,
  PROFILE: `${API_BASE_URL}/api/v1/auth/profile/`,
  PASSWORD_CHANGE: `${API_BASE_URL}/api/v1/auth/password/change/`,
  
  // Products
  PRODUCTS: `${API_BASE_URL}/api/v1/products/`,
  PRODUCT_CREATE: `${API_BASE_URL}/api/v1/products/create/`,
  MY_PRODUCTS: `${API_BASE_URL}/api/v1/products/my-products/`,
  FEATURED_PRODUCTS: `${API_BASE_URL}/api/v1/products/featured/`,
  TRENDING_PRODUCTS: `${API_BASE_URL}/api/v1/products/trending/`,
  
  // Categories
  CATEGORIES: `${API_BASE_URL}/api/v1/categories/`,
  CATEGORY_TREE: `${API_BASE_URL}/api/v1/categories/tree/`,
  
  // Chat
  CONVERSATIONS: `${API_BASE_URL}/api/v1/chat/conversations/`,
  MESSAGES: `${API_BASE_URL}/api/v1/chat/conversations/`,
  
  // Payments
  PAYMENTS: `${API_BASE_URL}/api/v1/payments/`,
  BOOST_PACKAGES: `${API_BASE_URL}/api/v1/payments/boost-packages/`,
  
  // Notifications
  NOTIFICATIONS: `${API_BASE_URL}/api/v1/notifications/`,
  NOTIFICATION_PREFERENCES: `${API_BASE_URL}/api/v1/notifications/preferences/`,
  
  // Reviews
  REVIEWS: `${API_BASE_URL}/api/v1/reviews/`,
  
  // File uploads
  UPLOAD: `${API_BASE_URL}/api/v1/upload/`,
};

// API utility functions
export const apiRequest = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('evolutionMarketToken');
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (token) {
    defaultHeaders.Authorization = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    
    // Handle token expiration
    if (response.status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('evolutionMarketRefreshToken');
      if (refreshToken) {
        const refreshResponse = await fetch(`${API_BASE_URL}/api/v1/auth/token/refresh/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: refreshToken }),
        });

        if (refreshResponse.ok) {
          const data = await refreshResponse.json();
          localStorage.setItem('evolutionMarketToken', data.access);
          
          // Retry original request with new token
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${data.access}`,
          };
          return fetch(url, config);
        }
      }
      
      // If refresh fails, clear auth data
      localStorage.removeItem('evolutionMarketToken');
      localStorage.removeItem('evolutionMarketRefreshToken');
      window.location.reload();
    }

    return response;
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
};

export default API_BASE_URL;