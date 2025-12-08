"use client";

import { useCallback } from "react";

import { apiFetch, type ApiRequestOptions } from "@/lib/api-client";
import { useAuthStore } from "@/lib/auth-store";

export function useApi() {
  const token = useAuthStore((state) => state.accessToken);

  return useCallback(
    async <T>(path: string, options: ApiRequestOptions = {}) => {
      return apiFetch<T>(path, {
        ...options,
        token: options.token ?? token ?? undefined,
      });
    },
    [token],
  );
}
