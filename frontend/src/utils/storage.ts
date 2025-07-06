// Storage utilities for managing user data and images

export interface StoredUser {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  isVerified: boolean;
  isAdmin: boolean;
  contactNumber?: string;
  createdAt: string;
}

export interface StoredProduct {
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
  location?: string;
  createdAt: string;
  isActive: boolean;
}

export interface StoredNotification {
  id: string;
  type: string;
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  productId?: string;
}

// User Storage
export const userStorage = {
  save: (user: StoredUser): void => {
    localStorage.setItem('evolutionMarketUser', JSON.stringify(user));
  },

  get: (): StoredUser | null => {
    const stored = localStorage.getItem('evolutionMarketUser');
    return stored ? JSON.parse(stored) : null;
  },

  remove: (): void => {
    localStorage.removeItem('evolutionMarketUser');
  },

  update: (updates: Partial<StoredUser>): void => {
    const current = userStorage.get();
    if (current) {
      const updated = { ...current, ...updates };
      userStorage.save(updated);
    }
  }
};

// Product Storage
export const productStorage = {
  save: (product: StoredProduct): void => {
    const products = productStorage.getAll();
    const updated = products.filter(p => p.id !== product.id);
    updated.push(product);
    localStorage.setItem('evolutionMarketProducts', JSON.stringify(updated));
  },

  getAll: (): StoredProduct[] => {
    const stored = localStorage.getItem('evolutionMarketProducts');
    return stored ? JSON.parse(stored) : [];
  },

  getById: (id: string): StoredProduct | null => {
    const products = productStorage.getAll();
    return products.find(p => p.id === id) || null;
  },

  getByUserId: (userId: string): StoredProduct[] => {
    const products = productStorage.getAll();
    return products.filter(p => p.sellerId === userId);
  },

  remove: (id: string): void => {
    const products = productStorage.getAll();
    const filtered = products.filter(p => p.id !== id);
    localStorage.setItem('evolutionMarketProducts', JSON.stringify(filtered));
  },

  update: (id: string, updates: Partial<StoredProduct>): void => {
    const products = productStorage.getAll();
    const index = products.findIndex(p => p.id === id);
    if (index !== -1) {
      products[index] = { ...products[index], ...updates };
      localStorage.setItem('evolutionMarketProducts', JSON.stringify(products));
    }
  }
};

// Image Storage (using base64 for demo - in production use cloud storage)
export const imageStorage = {
  save: async (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result as string;
        const imageId = `img_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        localStorage.setItem(`evolutionMarketImage_${imageId}`, base64);
        resolve(imageId);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  },

  get: (imageId: string): string | null => {
    return localStorage.getItem(`evolutionMarketImage_${imageId}`);
  },

  remove: (imageId: string): void => {
    localStorage.removeItem(`evolutionMarketImage_${imageId}`);
  },

  // Convert file to base64 URL for immediate display
  getPreviewUrl: (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
};

// Notification Storage
export const notificationStorage = {
  save: (notification: StoredNotification): void => {
    const notifications = notificationStorage.getAll();
    notifications.unshift(notification); // Add to beginning
    // Keep only last 100 notifications
    const trimmed = notifications.slice(0, 100);
    localStorage.setItem('evolutionMarketNotifications', JSON.stringify(trimmed));
    
    // Trigger storage event for real-time updates
    window.dispatchEvent(new Event('storage'));
  },

  getAll: (): StoredNotification[] => {
    const stored = localStorage.getItem('evolutionMarketNotifications');
    return stored ? JSON.parse(stored) : [];
  },

  markAsRead: (id: string): void => {
    const notifications = notificationStorage.getAll();
    const updated = notifications.map(n => 
      n.id === id ? { ...n, isRead: true } : n
    );
    localStorage.setItem('evolutionMarketNotifications', JSON.stringify(updated));
    window.dispatchEvent(new Event('storage'));
  },

  markAllAsRead: (): void => {
    const notifications = notificationStorage.getAll();
    const updated = notifications.map(n => ({ ...n, isRead: true }));
    localStorage.setItem('evolutionMarketNotifications', JSON.stringify(updated));
    window.dispatchEvent(new Event('storage'));
  },

  remove: (id: string): void => {
    const notifications = notificationStorage.getAll();
    const filtered = notifications.filter(n => n.id !== id);
    localStorage.setItem('evolutionMarketNotifications', JSON.stringify(filtered));
    window.dispatchEvent(new Event('storage'));
  },

  getUnreadCount: (): number => {
    const notifications = notificationStorage.getAll();
    return notifications.filter(n => !n.isRead).length;
  }
};

// Search History Storage
export const searchStorage = {
  save: (query: string): void => {
    if (!query.trim()) return;
    
    const searches = searchStorage.getAll();
    const filtered = searches.filter(s => s !== query);
    filtered.unshift(query);
    
    // Keep only last 10 searches
    const trimmed = filtered.slice(0, 10);
    localStorage.setItem('evolutionMarketSearches', JSON.stringify(trimmed));
  },

  getAll: (): string[] => {
    const stored = localStorage.getItem('evolutionMarketSearches');
    return stored ? JSON.parse(stored) : [];
  },

  clear: (): void => {
    localStorage.removeItem('evolutionMarketSearches');
  }
};

// Recently Viewed Storage
export const recentlyViewedStorage = {
  save: (productId: string): void => {
    const viewed = recentlyViewedStorage.getAll();
    const filtered = viewed.filter(id => id !== productId);
    filtered.unshift(productId);
    
    // Keep only last 20 items
    const trimmed = filtered.slice(0, 20);
    localStorage.setItem('evolutionMarketRecentlyViewed', JSON.stringify(trimmed));
  },

  getAll: (): string[] => {
    const stored = localStorage.getItem('evolutionMarketRecentlyViewed');
    return stored ? JSON.parse(stored) : [];
  },

  clear: (): void => {
    localStorage.removeItem('evolutionMarketRecentlyViewed');
  }
};

// Wishlist Storage
export const wishlistStorage = {
  add: (productId: string): void => {
    const wishlist = wishlistStorage.getAll();
    if (!wishlist.includes(productId)) {
      wishlist.push(productId);
      localStorage.setItem('evolutionMarketWishlist', JSON.stringify(wishlist));
    }
  },

  remove: (productId: string): void => {
    const wishlist = wishlistStorage.getAll();
    const filtered = wishlist.filter(id => id !== productId);
    localStorage.setItem('evolutionMarketWishlist', JSON.stringify(filtered));
  },

  getAll: (): string[] => {
    const stored = localStorage.getItem('evolutionMarketWishlist');
    return stored ? JSON.parse(stored) : [];
  },

  isInWishlist: (productId: string): boolean => {
    const wishlist = wishlistStorage.getAll();
    return wishlist.includes(productId);
  },

  clear: (): void => {
    localStorage.removeItem('evolutionMarketWishlist');
  }
};

// Clear all storage (for logout or reset)
export const clearAllStorage = (): void => {
  const keys = Object.keys(localStorage);
  keys.forEach(key => {
    if (key.startsWith('evolutionMarket')) {
      localStorage.removeItem(key);
    }
  });
};

export default {
  user: userStorage,
  product: productStorage,
  image: imageStorage,
  notification: notificationStorage,
  search: searchStorage,
  recentlyViewed: recentlyViewedStorage,
  wishlist: wishlistStorage,
  clearAll: clearAllStorage
};