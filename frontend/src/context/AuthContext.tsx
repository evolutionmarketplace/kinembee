import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types';
import { userStorage, clearAllStorage } from '../utils/storage';
import { API_ENDPOINTS } from '../config/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored user data and validate token
    const initializeAuth = async () => {
      try {
        const storedUser = userStorage.get();
        const token = localStorage.getItem('evolutionMarketToken');
        
        if (storedUser && token) {
          // Validate token with backend
          const response = await fetch(API_ENDPOINTS.PROFILE, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData.user || userData);
            userStorage.save(userData.user || userData);
          } else {
            // Token is invalid, clear storage
            clearAllStorage();
          }
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        clearAllStorage();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Login failed');
      }

      // Store user data and token
      const userData = data.user;
      const token = data.tokens?.access || data.access_token || data.token;

      if (!userData || !token) {
        throw new Error('Invalid response from server');
      }

      setUser(userData);
      userStorage.save(userData);
      localStorage.setItem('evolutionMarketToken', token);

      // Store refresh token if available
      if (data.tokens?.refresh || data.refresh_token) {
        localStorage.setItem('evolutionMarketRefreshToken', data.tokens.refresh || data.refresh_token);
      }

    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (name: string, email: string, password: string): Promise<void> => {
    try {
      const response = await fetch(API_ENDPOINTS.REGISTER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username: name,
          first_name: name.split(' ')[0] || name,
          last_name: name.split(' ').slice(1).join(' ') || '',
          email, 
          password,
          password_confirm: password,
          terms_accepted: true
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Registration failed');
      }

      // Store user data and token
      const userData = data.user;
      const token = data.tokens?.access || data.access_token || data.token;

      if (!userData || !token) {
        throw new Error('Invalid response from server');
      }

      setUser(userData);
      userStorage.save(userData);
      localStorage.setItem('evolutionMarketToken', token);

      // Store refresh token if available
      if (data.tokens?.refresh || data.refresh_token) {
        localStorage.setItem('evolutionMarketRefreshToken', data.tokens.refresh || data.refresh_token);
      }

    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      const token = localStorage.getItem('evolutionMarketToken');
      const refreshToken = localStorage.getItem('evolutionMarketRefreshToken');

      if (token) {
        // Attempt to logout on backend
        await fetch(API_ENDPOINTS.LOGOUT, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: refreshToken }),
        }).catch(() => {
          // Ignore logout errors, still clear local data
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always clear local data
      setUser(null);
      clearAllStorage();
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    if (!user) return;

    try {
      const token = localStorage.getItem('evolutionMarketToken');
      
      if (token) {
        // Update on backend
        const response = await fetch(API_ENDPOINTS.PROFILE, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        if (response.ok) {
          const updatedData = await response.json();
          const updatedUser = { ...user, ...updatedData };
          setUser(updatedUser);
          userStorage.save(updatedUser);
          return;
        }
      }

      // Fallback to local update if backend fails
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      userStorage.save(updatedUser);
      
    } catch (error) {
      console.error('Update user error:', error);
      // Fallback to local update
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      userStorage.save(updatedUser);
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      login,
      register,
      logout,
      updateUser,
      isLoading
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};