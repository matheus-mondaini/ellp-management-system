"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/lib/auth-store";

const schema = z.object({
  email: z.string().email({ message: "Informe um e-mail válido" }),
  password: z.string().min(8, "Senha mínima de 8 caracteres"),
});

type FormValues = z.infer<typeof schema>;

function LoginForm() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [redirectPath, setRedirectPath] = useState("/dashboard");
  const login = useAuthStore((state) => state.login);
  const status = useAuthStore((state) => state.status);
  const form = useForm<FormValues>({ resolver: zodResolver(schema) });

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const nextParam = params.get("next");
    setRedirectPath(nextParam && nextParam.startsWith("/") ? nextParam : "/dashboard");
  }, []);

  const onSubmit = async (values: FormValues) => {
    try {
      setError(null);
      await login(values);
      router.replace(redirectPath);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha na autenticação");
    }
  };

  return (
    <section className="space-y-6 text-left">
      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Acesso restrito</p>
        <h2 className="text-3xl font-semibold text-white">Portal Administrativo</h2>
        <p className="text-sm text-slate-300">
          Autentique-se para acompanhar as oficinas, inscrições e certificados do projeto ELLP.
        </p>
      </header>

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 rounded-2xl bg-white/5 p-6">
        <Input
          label="E-mail institucional"
          placeholder="admin@ellp.test"
          type="email"
          autoComplete="username"
          {...form.register("email")}
          error={form.formState.errors.email?.message}
        />
        <Input
          label="Senha"
          type="password"
          autoComplete="current-password"
          {...form.register("password")}
          error={form.formState.errors.password?.message}
        />
        {error && <p className="text-sm text-rose-300">{error}</p>}
        <Button type="submit" loading={status === "loading"} className="w-full">
          Entrar
        </Button>
      </form>
    </section>
  );
}

export default function LoginPage() {
  return <LoginForm />;
}
