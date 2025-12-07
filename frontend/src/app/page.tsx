import Link from "next/link";

const DOCS_BASE =
  "https://github.com/startse/integration-workshop/tree/main/ellp-management-system/docs";

const cards = [
  {
    title: "Requisitos",
    description: "Catálogo RF-001 ao RF-035 com foco no MVP",
    href: `${DOCS_BASE}/requirements.md`,
  },
  {
    title: "Arquitetura",
    description: "FastAPI + Supabase + Next.js",
    href: `${DOCS_BASE}/architecture.md`,
  },
  {
    title: "Testes",
    description: "Pyramid com pytest e Playwright",
    href: `${DOCS_BASE}/test-strategy.md`,
  },
];

export default function Home() {
  return (
    <section className="space-y-10">
      <header className="space-y-2">
        <p className="text-sm font-semibold uppercase tracking-wide text-sky-600">
          Planejamento
        </p>
        <h1 className="text-3xl font-bold text-slate-900">
          ELLP Management System
        </h1>
        <p className="text-base text-slate-600">
          Portal administrativo em Next.js integrado ao backend FastAPI e banco Supabase
          para controle de oficinas, presença e emissão de certificados.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-3">
        {cards.map((card) => (
          <article key={card.title} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">{card.title}</h2>
            <p className="mt-2 text-sm text-slate-600">{card.description}</p>
            <Link
              href={card.href}
              className="mt-4 inline-flex text-sm font-medium text-sky-600 hover:text-sky-700"
            >
              Ver documento →
            </Link>
          </article>
        ))}
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-xl font-semibold text-slate-900">Status</h2>
        <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-slate-600">
          <li>Backlog do MVP definido em `docs/requirements.md`.</li>
          <li>Arquitetura e cronograma descritos em `docs/architecture.md` e `docs/schedule.md`.</li>
          <li>Pipelines e estratégia de testes descritos em `docs/test-strategy.md`.</li>
        </ul>
      </section>
    </section>
  );
}
