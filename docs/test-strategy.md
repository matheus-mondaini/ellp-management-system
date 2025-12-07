# Estratégia de Testes Automatizados — ELLP Management System

> Versão 0.1 · Responsável: Matheus Mondaini · Data: 2025-12-07

## 1. Objetivos
Garantir qualidade contínua desde o planejamento, assegurando que os requisitos funcionais RF-001 a RF-035 sejam cobertos por testes automatizados, com feedback rápido (CI), rastreabilidade e critérios claros de saída por sprint.

## 2. Pirâmide de Testes
| Nível | Ferramentas | Cobertura alvo | Responsável |
|-------|-------------|----------------|-------------|
| Unitário | `pytest`, `pytest-asyncio`, `factory-boy` (futuro) | ≥ 70% sprint 1 · ≥ 80% sprint 2 | Backend devs |
| Integração/API | `httpx.AsyncClient`, `pytest` | Casos críticos (auth, inscrição, certificados) | Backend devs |
| Contrato | `schemathesis` (opcional), validação OpenAPI gerada pelo FastAPI | 100% dos endpoints críticos | QA/Dev |
| E2E Web | `Playwright` (headed + CI) | Fluxo feliz Sprint 1 · Fluxo completo Sprint 2 | Full-stack dev |
| Acessibilidade | `@axe-core/playwright` (futuro) | Páginas públicas e principais | Front dev |

## 3. Escopo por Sprint
### Sprint 1
- Testes unitários: serviços de auth, oficinas e inscrições.
- Integração: rotas `/auth`, `/users`, `/oficinas`, `/inscricoes`.
- E2E básico: login + criação de oficina.

### Sprint 2
- Ampliação para presenças, progressos e certificados.
- Playwright cobrindo fluxo completo (cadastro → certificado → validação pública).
- Testes de contrato para endpoints públicos (`/certificados/validar`).

## 4. Estrutura de Pastas
```
backend/
  tests/
    unit/
    integration/
    fixtures/
    e2e/ (API-level via httpx)
frontend/
  tests/
    unit/ (React Testing Library)
    e2e/  (Playwright)
.github/
  workflows/
    backend-ci.yml
    frontend-ci.yml
```

## 5. Critérios de Aceitação dos Testes
- **Unitário**: sem mocks excessivos; validações e regras de negócio isoladas.
- **Integração**: usa banco SQLite em memória ou Supabase schema no Testcontainers.
- **E2E**: roda contra ambiente docker-compose (`backend` + `frontend`).
- **Cobertura**: relatório `pytest --cov` publicado como artifact.
- **Documentação**: cada RF tem link para testes correspondentes no README/Project board.

## 6. Testes Prioritários (RF → Caso)
| Requisito | Caso de teste | Tipo |
|-----------|---------------|------|
| RF-019 | Login válido e inválido | Integração |
| RF-005 | Impedir inscrição duplicada | Unitário + Integração |
| RF-007 | Cálculo de presença (percentual) | Unitário |
| RF-032 | Conclusão automática disparando certificado | Integração |
| RF-008 | Geração de PDF (mock storage) | Unitário/Integração |
| RF-009 | Validação pública retorna 404 para hash inválido | Integração |
| RF-033 | Download autenticado do certificado | E2E |

## 7. Automatização em CI
- **backend-ci.yml**: `pip install -r requirements.txt`, `pytest --cov=app --cov-report=xml`, upload `coverage.xml`.
- **frontend-ci.yml**: `npm ci`, `npm run lint`, `npx playwright install --with-deps`, `npm run test:e2e` (futuro).
- **Quality Gates**: build falha se cobertura < 70% (Sprint 1) ou < 80% (Sprint 2).

## 8. Dados & Ambientes de Teste
- Banco dedicado (schema `ellp_test`) no Supabase ou `testcontainers` PostgreSQL.
- Seed inicial: usuários admin e professor, 1 oficina, 2 estudantes.
- Armazenamento: bucket `certificados-test` com política de limpeza diária.

## 9. Riscos e Planos de Mitigação
| Risco | Ação |
|-------|------|
| Dependência do Supabase em testes | Criar camada de repositório com mocks + usar PostgreSQL local quando offline |
| Geração de PDF lenta | Mockar camada de PDF em unit/integration; validar bytes somente em E2E |
| Playwright flakey no CI | Rodar em modo headless + usar `tracing=retain-on-failure` |
| Falta de tempo para cobertura | Automatizar templates `pytest` e `playwright codegen` |

## 10. Próximos Passos
1. Criar `backend/tests/unit` com factories de usuário.
2. Configurar banco efêmero com `pytest` fixtures.
3. Adicionar `frontend/tests/e2e/login.spec.ts` com Playwright.
4. Publicar badges de cobertura no README após Sprint 1.
