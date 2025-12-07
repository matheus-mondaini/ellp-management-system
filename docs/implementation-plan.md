# Plano de Implementação Incremental

> Referências: `docs/requirements.md`, `docs/architecture.md`, `docs/schema_supabase.sql`

## Objetivo Imediato (Sprint 1 · Dias 1-2)
Implementar o núcleo de autenticação e gestão de usuários utilizando FastAPI + SQLAlchemy sobre o schema Supabase, conforme RF-019, RF-001 e RF-002.

## Etapas Planejadas

1. **Fundamentos do Backend**
   - Criar `config.py` para carregar variáveis (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, segredos JWT etc.).
   - Criar `database.py` com engine/Session do SQLAlchemy apontando para o Postgres do Supabase (ou `DATABASE_URL` local compatível com `docs/schema_supabase.sql`).
   - Estruturar pastas conforme arquitetura (`models/`, `schemas/`, `routers/`, `services/`, `utils/`, `middlewares/`).

2. **Modelagem (Subset Inicial do Schema)**
   - Implementar modelos SQLAlchemy para `users`, `pessoas`, `alunos`, `tutores`, `professores`, respeitando tipos, constraints e relacionamentos do schema oficial.
   - Criar Pydantic Schemas para criação/leitura (`UserCreate`, `PessoaBase`, `AlunoCreate`, etc.).

3. **Camada de Segurança (RF-019, RF-002)**
   - `utils/security.py`: hash com bcrypt, geração/validação JWT (access + refresh) com expiração configurável.
   - `middlewares/auth_middleware.py`: dependências FastAPI `get_current_user`/`require_role` que consultam banco e aplicam RBAC.

4. **Serviços e Routers Prioritários**
   - `services/auth_service.py`: login, refresh, logout (opcional) usando Supabase DB.
   - `routers/auth.py`: endpoints `POST /auth/login`, `POST /auth/refresh`.
   - `services/user_service.py`: criação transacional de usuários + pessoa + especialização (Aluno/Tutor/Professor).
   - `routers/users.py`: endpoints `POST /users/{tipo}` e `GET` básicos.

5. **Testes Automatizados**
   - Fixtures (`backend/tests/conftest.py`) com banco temporário (SQLite compatível com schema ou Supabase test DB).
   - Testes: `test_auth.py` (sucesso/falha), `test_users.py` (criações e RBAC), garantindo início da cobertura.

6. **Integração com Supabase**
   - Adicionar instruções no README para executar `docs/schema_supabase.sql` e preencher `.env.example`.
   - Avaliar uso de Alembic ou script simples para garantir compatibilidade local.

## Critérios de Aceitação desta Entrega
- Estrutura de pastas igual ao blueprint de `docs/architecture.md` para o backend.
- Modelos/tabelas compatíveis com `docs/schema_supabase.sql` (ao menos `users`, `pessoas`, `alunos`, `tutores`, `professores`).
- Endpoints de login e criação de usuários funcionando com RBAC mínimo (admin cria perfis).
- Testes cobrindo fluxo feliz e cenários de erro para autenticação/usuários.
- Documentação atualizada (README + este plano) descrevendo como rodar a stack.

## Próximos Incrementos (após concluir esta etapa)
1. CRUD de temas e oficinas (RF-010, RF-003, RF-004, RF-011, RF-012).
2. Fluxos de inscrições (RF-005, RF-013) e presenças (RF-007, RF-031, RF-032).
3. Certificados + PDF + Storage (RF-008, RF-033, RF-034, RF-035, RF-009).
4. Relatórios, dashboard, auditoria e exportações (RF-014, RF-015, RF-022, RF-018, RF-021).
5. Frontend protegido (login, dashboards, CRUDs) consumindo os endpoints implantados.
