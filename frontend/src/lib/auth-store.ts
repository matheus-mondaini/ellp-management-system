'use client';

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

import { apiFetch } from './api-client';
import { type AuthenticatedUser, type LoginRequest, type TokenPair } from '@/types/api';

export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'error';

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  user: AuthenticatedUser | null;
  status: AuthStatus;
  error: string | null;
  hydrated: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  syncUser: () => Promise<AuthenticatedUser | null>;
  setHydrated: () => void;
  clearError: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      status: 'idle',
      error: null,
      hydrated: false,
      async login(credentials) {
        try {
          set({ status: 'loading', error: null });
          const tokens = await apiFetch<TokenPair>('/auth/login', {
            method: 'POST',
            data: credentials,
          });
          set({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token });
          await get().syncUser();
        } catch (error) {
          set({ status: 'error', error: error instanceof Error ? error.message : 'Falha no login', accessToken: null, refreshToken: null, user: null });
          throw error;
        }
      },
      logout() {
        set({ accessToken: null, refreshToken: null, user: null, status: 'idle', error: null });
      },
      async syncUser() {
        const token = get().accessToken;
        if (!token) {
          set({ user: null, status: 'idle' });
          return null;
        }
        try {
          const profile = await apiFetch<AuthenticatedUser>('/auth/me', { token });
          set({ user: profile, status: 'authenticated', error: null });
          return profile;
        } catch (error) {
          set({ accessToken: null, refreshToken: null, user: null, status: 'error', error: 'Sessão expirada. Faça login novamente.' });
          throw error;
        }
      },
      setHydrated() {
        set({ hydrated: true });
      },
      clearError() {
        set({ error: null });
      },
    }),
    {
      name: 'ellp-auth-store',
      storage: createJSONStorage(() => localStorage),
      onRehydrateStorage: () => (state, error) => {
        if (error) {
          console.error('Erro ao reidratar auth store', error);
        }
        state?.setHydrated();
      },
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
    },
  ),
);
