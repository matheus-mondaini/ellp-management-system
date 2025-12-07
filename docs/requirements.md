# Requisitos Funcionais - ELLP Management System

> Versão: 0.1 (Planejamento)
> Data: 2025-11-07
> Status global: Em elaboração
> Tema: Controle de oficinas (Professor, tutores, alunos, temas das oficinas, certificado)

## Visão Geral
O sistema ELLP Management System suportará o gerenciamento completo das oficinas do projeto de extensão ELLP, centralizando cadastro de pessoas, oficinas, inscrições, presença e emissão de certificados. Este documento lista os requisitos funcionais (RF) identificados, com breve descrição, prioridade e status inicial.

**Contexto importante**:
- **Alunos**: Crianças do ensino infantil da cidade e região
- **Tutores**: Professores, alunos da faculdade ou outros voluntários
- **Professores**: Responsáveis pelas oficinas
- **Administrador**: Responsável pelo sistema inicialmente. Cargo máximo, (e.g.: para coordenador(es) do projeto ELLP), em eventual necessidade de distingui-los dos professores

Legenda de Prioridade:
- **Alta**: Essencial para MVP / primeira entrega
- **Média**: Importante para operação regular
- **Baixa**: Incremental / pós-MVP

Status inicial: `planejado`

## Catálogo de Requisitos Funcionais (MVP)

### Módulo: Autenticação e Gestão de Usuários

*Mantive RBAC e relacionados como prioridade média pois inicialmente o sistema poderá ser direcionado apenas para administradores e professores/tutores, sem necessidade de auto-cadastro ou múltiplos perfis, apenas com acesso de um usuário admin.*


| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-001 | Cadastro de Perfis | Cadastrar usuários com perfis: Administrador, Professor, Tutor, Aluno (criança com dados do responsável) | Admin | Média | planejado |
| RF-002 | Gestão de Permissões | Restringir ações por perfil usando RBAC (Role-Based Access Control) | Admin | Média | planejado |
| RF-019 | Autenticação Usuário | Login/logout com JWT e refresh token | Usuário | Média | planejado |
| RF-020 | Recuperação de Senha | Fluxo para reset de senha via email | Usuário | Baixa | planejado |

### Módulo: Gestão de Temas e Oficinas

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-010 | Gestão de Temas | Cadastrar, editar e listar temas de oficinas (ex: "Scratch Básico", "Robótica com LEGO") | Admin/Professor | Alta | planejado |
| RF-003 | Cadastro de Oficinas | Criar/editar oficinas com: título, descrição, tema(s), carga horária, capacidade máxima, período (início/fim), local | Professor/Admin | Alta | planejado |
| RF-004 | Catálogo de Oficinas | Listar oficinas com filtros (tema, status, período) e informações de vagas | Admin/Professor/Tutor | Alta | planejado |
| RF-011 | Gestão de Tutores | Associar tutores a oficinas e controlar carga horária total | Admin/Professor | Alta | planejado |
| RF-012 | Gestão de Professores | Definir professor responsável por cada oficina | Admin | Alta | planejado |

### Módulo: Inscrições e Alunos

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-005 | Inscrição de Alunos | Permitir Admin/Professor/Tutor inscrever alunos em oficinas respeitando capacidade máxima (Como alunos são crianças, manterei inscrição como administrativa, para garantir segurança) | Admin/Professor/Tutor | Alta | planejado |
| RF-013 | Histórico de Participação | Consultar histórico completo de oficinas por aluno, tutor ou professor | Todos perfis | Alta | planejado |

### Módulo: Presença e Progresso

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-007 | Registro de Presença | Registrar presença por sessão/aula da oficina para cada aluno, calculando percentual automaticamente | Tutor/Professor | Alta | planejado |
| RF-031 | Controle de Progresso | Registrar status do aluno na oficina: Inscrito, Em Andamento, Concluído, Abandonou | Tutor/Professor | Alta | planejado |
| RF-032 | Conclusão Automática | Sistema marca oficina como concluída para aluno quando critérios são atingidos (presença mínima + status manual) | Sistema | Alta | planejado |

### Módulo: Certificados

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-008 | Emissão de Certificado (Aluno) | Gerar certificado de conclusão em PDF automaticamente após critérios atendidos (75% presença + conclusão) | Sistema | Alta | planejado |
| RF-033 | Download de Certificado (Aluno) | Permitir visualização e download do certificado do aluno em PDF | Admin/Professor | Alta | planejado |
| RF-034 | Emissão de Certificado (Tutor) | Gerar certificado de participação/tutoria em PDF para tutores/voluntários | Admin | Média | planejado |
| RF-035 | Download de Certificado (Tutor) | Permitir visualização e download do certificado de tutoria em PDF | Admin/Tutor | Média | planejado |
| RF-009 | Validação de Certificado | Disponibilizar endpoint/página pública para validar autenticidade do certificado via ID único | Público | Média | planejado |

### Módulo: Relatórios e Dashboard

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-014 | Relatório de Frequência | Gerar relatório consolidado de presença por oficina (individual e geral) | Professor/Admin | Média | planejado |
| RF-015 | Relatório de Certificados | Listar certificados emitidos e pendentes com filtros | Admin | Média | planejado |
| RF-022 | Dashboard Administrativo | Exibir métricas resumidas: oficinas ativas, total de inscrições, certificados emitidos, presença média | Admin | Média | planejado |

### Módulo: Auditoria e Segurança

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-021 | Auditoria de Ações | Registrar log de ações críticas (criação de oficina, inscrição, emissão de certificado, alteração de dados) | Sistema | Média | planejado |

### Módulo: Administração (Funcionalidades Auxiliares)

| ID | Título | Descrição | Ator Principal | Prioridade | Status |
|----|--------|-----------|----------------|------------|--------|
| RF-018 | Exportação de Dados | Exportar CSV/Excel de inscrições, presença e certificados para análise externa | Admin | Baixa | planejado |

## Requisitos Funcionais Opcionais (Pós-MVP / Backlog Futuro)

*Removidos do MVP para focar no escopo essencial. Podem ser implementados em versões futuras:*

| ID | Título | Observação |
|----|--------|-----------|
| RF-006 | Aprovação de Inscrições | Lista de espera - necessário apenas se houver processo seletivo ou necessidade de validação |
| RF-016 | Notificações de Status | Email para responsáveis - requer integração de email |
| RF-017 | Pesquisa Socioeconômica | Fora do tema "Controle de oficinas", mas podemos pensar em juntar diferentes temas posteriormente em um sistema maior |
| RF-023 | Gestão de Capacidade Dinâmica | Lista de espera dinâmica - complexidade desnecessária para MVP |
| RF-024 | Versionamento de Certificado | Implementar se surgir necessidade real de reemissão |
| RF-025 | Busca Global | Funcionalidade de conveniência |
| RF-026 | Verificação de Pré-requisitos | Adiciona complexidade - oficinas inicialmente independentes |
| RF-027 | Upload de Recursos | Materiais didáticos - pode ser Google Drive externo inicialmente |
| RF-028 | Visualização de Materiais | Complemento do RF-027 |
| RF-029 | Termo de Voluntariado | Coberto por RF-034/035 (certificado de tutor) |
| RF-030 | Gestão de Escolas | Fora do tema escolhido |

## Regras de Negócio


1. **Presença mínima**: 75% de presença requerida para emissão de certificado de conclusão
2. **Capacidade de oficina**: Inscrições respeitam capacidade máxima definida (sem lista de espera no MVP)
3. **Carga horária de tutor**: Um tutor não pode exceder carga horária máxima semanal configurável (sugestão: 20h/semana)
4. **Certificado único**: Cada certificado possui identificador único (hash/UUID) verificável publicamente
5. **Tipos de certificado**: 
   - **Certificado de Conclusão**: Para alunos que completaram a oficina
   - **Certificado de Participação**: Para tutores/voluntários que ministraram a oficina
6. **Conclusão de oficina para aluno**: Oficina é marcada como "Concluída" quando:
   - Presença ≥ 75% E
   - Status manual definido como "Concluído" pelo Tutor/Professor
7. **Dados do responsável**: Todo aluno (criança) deve ter dados do responsável cadastrados (nome, email, telefone)
8. **Período da oficina**: Oficinas têm data de início e fim. Após o fim, não aceitam novas inscrições
9. **Auditoria**: Ações críticas são registradas com timestamp e usuário responsável

## Modelo de Dados (Resumo)

### Principais Entidades:
- **users**: id, nome, email, senha_hash, role (admin, professor, tutor, aluno), telefone, dados_responsavel (se aluno)
- **temas**: id, nome, descricao
- **oficinas**: id, titulo, descricao, carga_horaria, capacidade_max, data_inicio, data_fim, local, status, professor_id
- **oficina_temas** (relacionamento N:N): oficina_id, tema_id (N:N)
- **oficina_tutores**: oficina_id, tutor_id (N:N)
- **inscricoes** (aluno + oficina + progresso + presença): id, aluno_id, oficina_id, data_inscricao, status (inscrito, em_andamento, concluido, abandonou), percentual_presenca
- **presencas** (registro por sessão/aula): id, inscricao_id, data_aula, presente (bool)
- **certificados** (PDF armazenado no Supabase Storage): id, inscricao_id OU tutor_id, tipo (aluno/tutor), data_emissao, hash_validacao, arquivo_pdf_url

## Stack Tecnológica

### Backend:
- **Linguagem**: Python 3.11+
- **Framework**: FastAPI - leve, rápido, ótimo para APIs RESTful (em testes, provou-se superior ao Django e Flask para MVPs e, já tenho experiência com ele)
- **Autenticação**: JWT
- **Geração de PDF**: ReportLab ou WeasyPrint para certificados (ao decorrer do projeto, escolherei a melhor opção para PDFs estilizados)
- **Validação**: Pydantic
- **Testes**: pytest
- **Supabase** (tem cliente Python oficial)

### Banco de Dados:
- **Supabase** (PostgreSQL nativo - excelente para relações complexas e escalável)
- **ORM**: SQLAlchemy ou Supabase Python Client
- **Storage**: Supabase Storage (para PDFs dos certificados)
- **Auth**: Pode usar Supabase Auth ou JWT próprio
- Row Level Security (RLS) para permissões

### Frontend:
- **Linguagem**: TypeScript - recomendado para type safety (já tenho experiência com React e Next.js, o que facilitará o desenvolvimento do frontend, além de já ter trabalhado com PostgreSQL em projetos anteriores, o que ajudará na modelagem do banco de dados)
- **Framework**: Next.js 15+ (App Router)
- **Estilização**: Tailwind CSS
- **Cliente**: Supabase JavaScript Client
- **Gerenciamento de Estado**: Zustand
- **Formulários**: React Hook Form + Zod

### DevOps:
- **Repositório**: GitHub (público)
- **CI/CD**: GitHub Actions
- **Deploy Backend**: Railway, Render ou Vercel (serverless)
- **Deploy Frontend**: Vercel
- **Kanban**: GitHub Projects

## Arquitetura (Alto Nível)

```
┌─────────────────┐
│   Next.js App   │
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS/REST
         │
┌────────▼────────┐       ┌──────────────┐
│  FastAPI        │◄──────┤   Supabase   │
│  (Backend/API)  │       │  PostgreSQL  │
└────────┬────────┘       └──────────────┘
         │
         │ Gera PDF
         ▼
┌─────────────────┐
│ Supabase Storage│
│ (Certificados)  │
└─────────────────┘
```

## Estratégia de Testes

### Backend (pytest):
- Testes unitários: Lógica de negócio (cálculo de presença, geração de hash)
- Testes de integração: Endpoints da API
- Testes de banco: Queries e relacionamentos
- Cobertura mínima: 80%

### Frontend:
- Testes de componentes: React Testing Library
- Testes E2E: Playwright (opcional, se houver tempo)

## Cronograma (2 Sprints)

### Sprint 1 - Fundação e Cadastros (2-3 semanas):
**Objetivo**: Sistema funcional com CRUD completo

- Configuração do ambiente (Supabase, FastAPI, Next.js)
- RF-001: Cadastro de Perfis
- RF-002: Gestão de Permissões
- RF-019: Autenticação (JWT)
- RF-010: Gestão de Temas
- RF-003: Cadastro de Oficinas
- RF-011/012: Gestão de Tutores e Professores
- RF-005: Inscrição de Alunos
- RF-004: Catálogo de Oficinas
- Testes automatizados básicos
- README e documentação da API (OpenAPI)

**Entregáveis**:
- API funcional com autenticação
- Interface para cadastros básicos
- Schema do banco no Supabase
- Vídeo de 3 minutos mostrando funcionalidades

### Sprint 2 - Presença, Certificados e Relatórios (2-3 semanas):
**Objetivo**: Fluxo completo de oficina até certificado

- RF-007: Registro de Presença
- RF-031: Controle de Progresso
- RF-032: Conclusão Automática
- RF-008: Emissão de Certificado (Aluno)
- RF-033: Download de Certificado (Aluno)
- RF-034/035: Certificado de Tutor
- RF-009: Validação de Certificado
- RF-014: Relatório de Frequência
- RF-015: Relatório de Certificados
- RF-022: Dashboard Administrativo
- RF-013: Histórico de Participação
- RF-021: Auditoria de Ações
- Testes de cobertura (>80%)
- Ajustes e refinamentos

**Entregáveis**:
- Sistema completo e funcional
- Certificados em PDF funcionando
- Relatórios implementados
- Vídeo de 3 minutos mostrando fluxo completo
- Documentação completa

### Revisão/Recuperação (1 semana):
- Correção de bugs apontados pelo professor
- Implementação de ajustes solicitados
- Melhorias na cobertura de testes
- Refinamento da documentação

## Critérios de Aceitação (Gerais)

1. **Código**: Clean code, seguindo PEP 8 (Python) e ESLint (JS/TS)
2. **Commits**: Mensagens descritivas e seguindo convenção (e.g., Conventional Commits)
3. **Issues**: Funcionalidades documentadas como issues no GitHub
4. **Kanban**: Board atualizado refletindo progresso real
5. **Testes**: Cobertura mínima de 80% no backend
6. **Documentação**: README completo com instruções de setup
7. **API**: Documentação OpenAPI/Swagger acessível
8. **Segurança**: Senhas com hash, JWT seguro, validação de inputs
9. **LGPD**: Consentimento para dados de responsáveis, possibilidade de exclusão

## Próximos Passos

1. ✅ Validar requisitos
2. ✅ Criar diagrama de arquitetura detalhado
3. ✅ Definir schema completo do banco no Supabase
4. ✅ Configurar repositório GitHub com template
5. ✅ Setup do ambiente de desenvolvimento
6. ✅ Definir padrões de código e style guides
7. ✅ Criar template de certificado (design)
8. ✅ Kickoff do Sprint 1
