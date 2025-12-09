# Plano Único de Testes — ELLP Management System

> Última atualização: 2025-12-08 · Responsável: Equipe ELLP · Fonte dos requisitos: `docs/requirements.md` · Diretrizes arquiteturais: `docs/architecture.md`

## 1. Contexto e Escopo
- **Arquitetura**: solução em 3 camadas (Frontend Next.js → Backend FastAPI → PostgreSQL/Supabase). Cada camada possui testes dedicados seguindo a estratégia definida em `docs/test-strategy.md`.
- **Objetivo**: garantir que os requisitos funcionais RF-001 a RF-035 estejam cobertos por casos de teste automatizados, com ênfase em RF críticos (autenticação, oficinas, inscrições, certificados e dashboard) e rastreabilidade completa.
- **Abrangência deste documento**: descreve conceitos-chave, casos de teste mapeados por requisito, evidências de cobertura (`test-results/backend-pytest-report.txt`) e comandos oficiais de execução.

## 2. Conceitos-Chave Aplicados
- **Caso de Teste (CT)**: especificação completa (pré-condições, passos, resultado esperado) implementada em testes automatizados Pytest ou Playwright.
- **Cenário de Teste**: agrupamento lógico de casos que validam um requisito (ex.: Autenticação reúne CT-001 a CT-003).
- **Camada de Teste**: nível da pirâmide (unitário, integração/API, E2E). Cada requisito escolhe a camada com melhor custo-benefício.
- **Dado Controlado**: fixtures do Pytest e seeds do Supabase garantindo isolamento (usuário admin, professor, oficinas demo).
- **Critério de Saída**: 100% dos casos planejados executados + cobertura global ≥ 90% (atual: 94%).

## 3. Matriz Requisito × Casos de Teste
| RF | Cenário / Caso de Teste | Arquivo / Identificador | Camada |
|----|-------------------------|-------------------------|--------|
| RF-019 (Autenticação) | CT-001 Login válido · CT-002 Login inválido · CT-003 Token inválido | `backend/tests/test_auth.py::test_login_success`, `test_login_fail_invalid_credentials`, `test_refresh_invalid_token` | Integração |
| RF-001/RF-012 (Usuários/Professores) | CT-010 Cadastro professor · CT-011 Validação campos obrigatórios | `backend/tests/test_professores.py` | Unidade + Integração |
| RF-003/RF-010 (Oficinas/Temas) | CT-020 Criar oficina · CT-021 Listar por tema · CT-022 Regra de capacidade | `backend/tests/test_oficinas.py`, `backend/tests/test_temas.py` | Unidade |
| RF-005/RF-031 (Inscrições/Status) | CT-030 Inscrição válida · CT-031 Bloqueio duplicidade · CT-032 Avanço de status | `backend/tests/test_inscricoes.py` | Integração |
| RF-022 (Dashboard) | CT-040 Métricas exibidas pós-login | `frontend/tests/e2e/dashboard.spec.ts::admin consegue autenticar...` | E2E |
| RF-009 (Validação Certificado) | CT-050 Hash inexistente retorna 404 | `backend/tests/test_certificados.py::test_validacao_hash_inexistente` | Integração |
| RF-008 (Certificados) | CT-060 Geração PDF aluno | `backend/test_pdf_generation.py` | Unidade |
| RF-033 (Download Certificado) | CT-070 Fluxo download autenticado | `frontend/tests/e2e/validar.spec.ts` | E2E |

> **Observação**: cada CT aponta explicitamente para o requisito no corpo do teste (docstring ou nome), permitindo rastreabilidade bidirecional.

## 4. Descrição dos Cenários Principais
1. **Autenticação (RF-019)**
   - Pré-condição: usuário `admin@ellp.test` ativo no Supabase (seed). 
   - Passos: enviar POST `/auth/login` com credenciais válidas, validar HTTP 200 e tokens JWT; repetir com credenciais inválidas (espera 401). 
   - Resultados: tokens persistidos no `useAuthStore`; revalidação via `/auth/me`.
2. **Gestão de Oficinas (RF-003/RF-010)**
   - Fixtures criam temas e professores. Tests verificam CRUD, associação a professor, limites de datas e capacidade.
3. **Inscrições e Progresso (RF-005/RF-031)**
   - Usa `InscricaoService`. Garante que aluno não exceda capacidade, atualiza status para “Concluído” ao atingir critérios.
4. **Dashboard Operacional (RF-022)**
   - Playwright executa login → navega `/dashboard` → valida cards “Oficinas ativas”, “Inscrições totais”, “Certificados emitidos”. Valor é comparado com regex numérico.
5. **Certificados e Validação Pública (RF-008/RF-009/RF-033)**
   - Pytest simula geração de PDF com storage mockado. Caso de validação garante 404 para hash desconhecido, 200 para existente. Frontend E2E cobre tela pública `/validar/[hash]`.

## 5. Cobertura Atual
- **Backend Pytest** (relatório completo em `test-results/backend-pytest-report.txt`):
  - 40 casos executados, 0 falhas, tempo total 26.18s.
  - Cobertura média: **94%** (`app` inteiro). Pontos de atenção: `app/database.py` (67%) e algumas rotas de usuários (76%).
  - Warnings: depreciações Pydantic Config e `datetime.utcnow()` (monitorados, não impactam aprovação).
- **Frontend Playwright**:
  - Casos chaves: `dashboard.spec.ts`, `home.spec.ts`, `validar.spec.ts`. Cada spec cobre ao menos um RF crítico (login, criação de oficina via UI mockada, validação de certificado).
  - Execuções salvam rastros em `frontend/test-results/*/error-context.md` quando ocorre falha.

## 6. Comandos Oficiais de Execução
### 6.1 Preparação Comum
```bash
# subir Supabase e dependências
cd /Users/startse/Documents/Estudos/UTFPR/integration-workshop
supabase start

# subir backend FastAPI (usa .env raiz)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6.2 Testes Backend (Unit + Integração)
```bash
cd backend
source .venv/bin/activate
pytest --cov=app --cov-report=xml --maxfail=1
```
- Artefatos: `coverage.xml`, log consolidado em `test-results/backend-pytest-report.txt` (copiar após execução para rastreabilidade).

### 6.3 Testes Frontend (E2E Playwright)
```bash
cd frontend
npm install   # ou npm ci no CI
npm run lint
npx playwright install --with-deps
npm run test:e2e     # alias para npx playwright test --reporter=html,line
```
- Em modo desenvolvimento (hot reload), manter `npm run dev` no frontend e `uvicorn` no backend antes de executar os testes.
- Artefatos: `playwright-report/`, `test-results/<spec>/error-context.md`, vídeos/trace quando `CI=1`.

## 7. Gestão de Dados e Ambientes
- **Variáveis de ambiente**: `.env` (raiz) sincroniza Supabase + frontend (`NEXT_PUBLIC_API_URL=http://localhost:8000`). Arquivos devem ser carregados antes dos testes.
- **Seed obrigatório**: usuário `admin@ellp.test`/`admin12345` e oficina demo (executar script SQL ou usar fixtures do Pytest).
- **Isolamento**: cada suíte Pytest recria transações para não persistir sujeira; Playwright reseta API mock via `tests/e2e/utils.ts::resetMockApi`.

---
Este documento é a referência única de testes para o projeto. Atualize-o sempre que:
- novos requisitos forem aprovados;
- novos casos automatizados forem adicionados; ou
- métricas de cobertura mudarem significativamente.
