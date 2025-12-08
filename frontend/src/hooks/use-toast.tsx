"use client";

import { useState, useCallback } from "react";

export type Toast = {
  id: string;
  title: string;
  description?: string;
  variant?: "default" | "success" | "error";
};

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((toast: Omit<Toast, "id">) => {
    setToasts((previous) => [
      ...previous,
      { id: crypto.randomUUID(), ...toast },
    ]);
  }, []);

  const dismiss = useCallback((id: string) => {
    setToasts((previous) => previous.filter((toast) => toast.id !== id));
  }, []);

  return { toasts, addToast, dismiss };
}
