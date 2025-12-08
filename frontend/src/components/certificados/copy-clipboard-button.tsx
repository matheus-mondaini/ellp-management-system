"use client";

import { Check, Copy } from "lucide-react";
import { useState, type ReactNode } from "react";

import { Button } from "@/components/ui/button";

type CopyClipboardButtonProps = {
  value: string;
  children: ReactNode;
};

export function CopyClipboardButton({ value, children }: CopyClipboardButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Erro ao copiar para a área de transferência", error);
    }
  };

  return (
    <Button
      type="button"
      variant="ghost"
      onClick={handleCopy}
      className="flex items-center gap-2 rounded-full border border-white/20 px-4 text-xs uppercase tracking-[0.3em] text-white/70 hover:border-white/50"
    >
      {copied ? <Check className="h-4 w-4 text-emerald-300" /> : <Copy className="h-4 w-4" />}
      {children}
    </Button>
  );
}
