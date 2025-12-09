"use client";

import { useEffect, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";

import { motion } from "framer-motion";
import { useShallow } from "zustand/react/shallow";

import { useAuthStore } from "@/lib/auth-store";

export function AuthGate({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { accessToken, hydrated, status, user, syncUser, error } = useAuthStore(
    useShallow((state) => ({
      accessToken: state.accessToken,
      hydrated: state.hydrated,
      status: state.status,
      user: state.user,
      syncUser: state.syncUser,
      error: state.error,
    })),
  );

  useEffect(() => {
    if (!hydrated || !accessToken || user) {
      return;
    }
    void syncUser();
  }, [hydrated, accessToken, user, syncUser]);

  useEffect(() => {
    if (!hydrated) return;
    if (!accessToken) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [hydrated, accessToken, router, pathname]);

  if (!hydrated || status === "loading" || (accessToken && !user)) {
    return (
      <motion.div
        className="flex min-h-[60vh] items-center justify-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <span className="rounded-full border border-emerald-200 px-4 py-2 text-sm text-emerald-700">
          Validando sessão…
        </span>
      </motion.div>
    );
  }

  if (!accessToken) {
    return null;
  }

  if (status === "error" && error) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center space-y-2 text-center text-rose-200">
        <p className="text-sm font-semibold">{error}</p>
        <button
          type="button"
          className="text-xs uppercase tracking-[0.4em] text-white/70 underline"
          onClick={() => router.replace(`/login?next=${encodeURIComponent(pathname)}`)}
        >
          refazer login
        </button>
      </div>
    );
  }

  return <>{children}</>;
}
