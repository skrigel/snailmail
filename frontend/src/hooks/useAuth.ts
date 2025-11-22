/**
 * Authentication hook for managing user session
 */

import { useState, useEffect } from 'react';
import { getAuthStatus, loginWithGoogle, logout } from '@/lib/api';

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true,
  });

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const data = await getAuthStatus();
      setAuthState({
        isAuthenticated: data.authenticated,
        user: data.user || null,
        loading: false,
      });
    } catch (error) {
      console.error('Failed to check auth status:', error);
      setAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
      });
    }
  };

  const login = () => {
    loginWithGoogle();
  };

  const handleLogout = () => {
    logout();
  };

  return {
    ...authState,
    login,
    logout: handleLogout,
    refresh: checkAuthStatus,
  };
}