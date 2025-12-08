"use client";

import { LogOut } from "lucide-react";

import { useAuthStore } from "@/lib/auth-store";
import { Button } from "@/components/ui/button";

export function LogoutButton() {
  const logout = useAuthStore((state) => state.logout);

  return (
    <Button
      variant="ghost"
      className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 text-xs uppercase tracking-[0.3em] text-white/70 hover:border-white/30 hover:text-white"
      onClick={() => logout()}
    >
      <LogOut className="h-4 w-4" />
      sair
    </Button>
  );
}
