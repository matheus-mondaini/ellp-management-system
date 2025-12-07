# Stack Tecnológico — ELLP Management System

| Camada | Tecnologia | Motivação |
|--------|------------|-----------|
| Frontend | **Next.js 15 (App Router) + TypeScript + Tailwind CSS** | Produtividade com React, suporte a SSR/SSG para página pública de validação e aderência ao background do time (JS/TS). Tailwind acelera protótipos com consistência visual. |
| State/Data | **React Query + Zustand + React Hook Form + Zod** | React Query para cache de requisições (oficinas, certificados), Zustand para estado global simples (auth), RHF + Zod para validação tipada de formulários administrativos. |
| Backend | **FastAPI (Python 3.11)** | Sintaxe moderna, tipagem forte (Pydantic), geração automática de OpenAPI, alta performance. Combina com expertise do time (Python para Data/ML). |
| ORM & Camada de Dados | **SQLAlchemy 2.x + Alembic (futuro)** | Suporte a Class Table Inheritance e transações complexas. Alembic garante versionamento do schema. |
| Banco & Storage | **Supabase (PostgreSQL + Storage + Auth)** | Hosting gerenciado, RLS nativo, storage para PDFs dos certificados e APIs compatíveis com Python/JS. |
| Autenticação | **JWT (access + refresh)** emitidos pelo FastAPI + RBAC | Mantém controle de perfis (admin, professor, tutor). Supabase Auth opcional para login social no futuro. |
| Documentação | **OpenAPI/Swagger** (via FastAPI) + `docs/architecture.md` + ADRs | Rastreabilidade técnica e comunicação com stakeholders. |
| Testes Backend | **pytest, pytest-asyncio, httpx, pytest-cov** | Cobertura de regras de negócio e rotas assíncronas. |
| Testes Frontend | **Playwright, React Testing Library, Vitest** (futuro) | Garantia de UX consistente e fluxo fim a fim. |
| PDFs | **ReportLab (default) ou WeasyPrint (fallback)** | Templates customizados com logotipos do ELLP, controle total do layout dos certificados. |
| Observabilidade | **Loguru/structlog + Supabase audit** | Logs estruturados e trilha de auditoria (RF-021). |
| Infra | **Docker, Docker Compose, GitHub Actions** | Reprodutibilidade local e pipelines de CI/CD.

## Decisões Arquiteturais
1. **FastAPI + Supabase**: Equilibra rapidez de desenvolvimento com robustez (PostgreSQL) e permite usar Python, tecnologia dominante do time.
2. **Next.js App Router**: Simplifica rotas protegidas e página pública (`/validar/[hash]`) com Server Components.
3. **Class Table Inheritance** para usuários (admins, professores, tutores, alunos) garantindo normalização e extensibilidade.
4. **Supabase Storage**: evita dependência de S3 durante o MVP e integra com policies RLS.
5. **Docker-first**: `docker-compose up` levanta backend e frontend sem dependências extras, facilitando demonstrações.

## Ferramentas Auxiliares
- **Task runners**: `make` (planejado) para comandos frequentes (`make dev`, `make test`).
- **Qualidade**: `ruff` (planejado) para lint Python, `eslint`/`prettier` para frontend.
- **Design**: Figma para template de certificado, exportado em SVG para ReportLab.

## Próximos Passos
1. Registrar ADRs (`docs/adrs/`) para as decisões críticas (FastAPI x Django, ReportLab x WeasyPrint, Supabase x RDS).
2. Configurar `Makefile` com targets `dev`, `test`, `lint`.
3. Avaliar adicionar Redis para filas de geração de certificados em versões futuras.
