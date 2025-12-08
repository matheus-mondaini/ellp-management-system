import Link from "next/link";
import { motion } from "framer-motion";

export default function LandingPage() {
  const cards = [
    {
      title: "Planejamento",
      description: "Requisitos, arquitetura e cronograma do sistema",
      href: "https://github.com/startse/integration-workshop/tree/main/ellp-management-system/docs",
    },
    {
      title: "Validação Pública",
      description: "Página dedicada para verificar autenticidade dos certificados",
      href: "/validar/demo-cert",
    },
    {
      title: "Portal Administrativo",
      description: "Acesso restrito para gestão de oficinas e participantes",
      href: "/login",
    },
  ];

  return (
    <div className="space-y-8">
      <motion.div
        className="grid gap-6 md:grid-cols-3"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0, y: 20 },
          visible: {
            opacity: 1,
            y: 0,
            transition: { staggerChildren: 0.1 },
          },
        }}
      >
        {cards.map((card) => (
          <motion.article
            key={card.title}
            variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}
            className="rounded-3xl border border-white/10 bg-white/5 p-5 text-left">
            <h2 className="text-lg font-semibold text-white">{card.title}</h2>
            <p className="mt-2 text-sm text-slate-300">{card.description}</p>
            <Link href={card.href} className="mt-4 inline-flex text-sm font-semibold text-emerald-300">
              Acessar →
            </Link>
          </motion.article>
        ))}
      </motion.div>
    </div>
  );
}
