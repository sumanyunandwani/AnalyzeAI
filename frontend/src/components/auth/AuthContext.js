import React, { createContext, useState, useContext, useEffect } from 'react';
import { API_ENDPOINTS } from '../../config/api';

const AuthContext = createContext({});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in from localStorage/sessionStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    
    // Check for OAuth callback parameters in URL
    checkOAuthCallback();
    
    // Check authentication status with backend
    checkAuthStatus();
  }, []);

  const checkOAuthCallback = async () => {
    // Check if we're returning from OAuth provider
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    
    if (code) {
      try {
        // Handle OAuth callback
        const response = await fetch(API_ENDPOINTS.AUTH_CALLBACK, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code, state }),
          credentials: 'include'
        });

        if (response.ok) {
          const data = await response.json();
          if (data.name && data.email) {
            login(data);
            // Clean up URL
            window.history.replaceState({}, document.title, window.location.pathname);
          }
        }
      } catch (error) {
        console.error('OAuth callback error:', error);
      }
    }
  };

  const checkAuthStatus = async () => {
    try {
      // Check if user is authenticated with backend
      const response = await fetch(API_ENDPOINTS.AUTH_STATUS, {
        method: 'GET',
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        // Your API returns user data directly if authenticated
        if (data.name && data.email) {
          const userData = {
            name: data.name,
            email: data.email,
            // Add any other fields from the response
            id: data.id || data.email, // Use email as ID if no ID provided
            provider: data.provider || 'oauth'
          };
          setUser(userData);
          localStorage.setItem('user', JSON.stringify(userData));
        }
      } else if (response.status === 401) {
        // User is not authenticated
        setUser(null);
        localStorage.removeItem('user');
      }
    } catch (error) {
      console.error('Auth status check error:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = (userData) => {
    const user = {
      name: userData.name,
      email: userData.email,
      id: userData.id || userData.email,
      provider: userData.provider || 'oauth'
    };
    setUser(user);
    localStorage.setItem('user', JSON.stringify(user));
  };

  const logout = async () => {
    try {
      // Call backend logout endpoint
      await fetch(API_ENDPOINTS.LOGOUT, {
        method: 'POST',
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    setUser(null);
    localStorage.removeItem('user');
  };

  const value = {
    user,
    login,
    logout,
    loading,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
