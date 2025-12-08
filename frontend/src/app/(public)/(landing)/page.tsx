import Link from "next/link";
import { motion } from "framer-motion";

const DOCS_BASE = "https://github.com/startse/integration-workshop/tree/main/ellp-management-system/docs";

const cards = [
  {
    title: "Requisitos",
    description: "Catálogo RF-001 ao RF-035",
    href: `${DOCS_BASE}/requirements.md`,
  },
  {
    title: "Arquitetura",
    description: "Visão FastAPI + Next.js + Supabase",
    href: `${DOCS_BASE}/architecture.md`,
  },
  {
    title: "Estratégia de Testes",
    description: "Piramide com pytest e Playwright",
    href: `${DOCS_BASE}/test-strategy.md`,
  },
];

export default function LandingPage() {
  return (
    <section className="space-y-12">
      <header className="space-y-3 text-center">
        <p className="text-xs uppercase tracking-[0.6em] text-emerald-300">Planejamento</p>
        <h1 className="text-4xl font-semibold text-white">ELLP Management System</h1>
        <p className="text-base text-slate-300">
          Portal administrativo integrado ao backend FastAPI e Supabase para controle das oficinas extensionistas.
        </p>
      </header>

      <motion.div
        className="grid gap-6 md:grid-cols-3"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: {},
          visible: {
            transition: { staggerChildren: 0.1 },
          },
        }}
      >
        {cards.map((card) => (
          <motion.article
            key={card.title}
            variants={{ hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0 } }}
            className="rounded-3xl border border-white/10 bg-white/5 p-5 text-left"
          >
            <h2 className="text-lg font-semibold text-white">{card.title}</h2>
            <p className="mt-2 text-sm text-slate-300">{card.description}</p>
            <Link href={card.href} className="mt-4 inline-flex text-sm font-semibold text-emerald-300">
              Ver documento →
            </Link>
          </motion.article>
        ))}
      </motion.div>

      <section className="rounded-[2.5rem] border border-white/10 bg-white/5 p-8 text-left">
        <h2 className="text-xl font-semibold text-white">Status do Planejamento</h2>
        <ul className="mt-4 space-y-2 text-sm text-slate-300">
          <li>✔️ Requisitos RF-001..RF-035 versionados em `docs/requirements.md`.</li>
          <li>✔️ Arquitetura em camadas documentada em `docs/architecture.md`.</li>
          <li>✔️ Estratégia de testes e pirâmide definidas em `docs/test-strategy.md`.</li>
        </ul>
      </section>
    </section>
  );
}
