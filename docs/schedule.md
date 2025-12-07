# Cronograma de Planejamento — ELLP Management System

> Período estimado: 7 semanas · Atualizado em 2025-12-07

## Linha do Tempo Geral
| Semana | Fase | Objetivos principais |
|--------|------|----------------------|
| 0 | Planejamento | Refinar requisitos, desenhar arquitetura, preparar ambiente |
| 1 | Setup Técnico | Supabase, FastAPI skeleton, Next.js scaffold, CI inicial |
| 2-3 | Sprint 1 | Cadastros + Autenticação + Inscrições (RF-001..RF-013) |
| 4-5 | Sprint 2 | Presenças + Certificados + Relatórios (RF-007..RF-022) |
| 6 | Homologação | Correções pós-feedback (se houver), otimização de testes |
| 7 | Entrega Final | Documentação, vídeo demonstrativo, handoff |

## Sprint Breakdown
### Sprint 1 — Fundação (2 semanas)
- **Meta**: Sistema administrativo funcional (login, oficinas, inscrições).
- **Backlog chave**: RF-001, RF-002, RF-003, RF-004, RF-005, RF-010, RF-011, RF-012, RF-013, RF-019.
- **Entregáveis**:
  - API FastAPI com CRUDs principais.
  - Frontend com login e telas de cadastro.
  - Testes unitários + integração cobrindo auth/officinas.
  - Vídeo de 3 minutos demonstrando fluxo de cadastro.

### Sprint 2 — Fluxo Completo (2 semanas)
- **Meta**: Do registro de presença à emissão do certificado.
- **Backlog chave**: RF-007, RF-031, RF-032, RF-008, RF-033, RF-034, RF-035, RF-009, RF-014, RF-015, RF-022, RF-021.
- **Entregáveis**:
  - Registro de presença, progresso e conclusão automática.
  - Geração de PDFs e validação pública.
  - Dashboard + relatórios.
  - Playwright E2E rodando no CI.

### Semana 6 — Homologação
- Correção dos apontamentos do professor
- Ajustes de performance e acessibilidade.
- Revisão de LGPD e auditoria.

### Semana 7 — Entrega Final
- Documentação atualizada (`README`, `docs/*`, OpenAPI).
- Vídeo final com fluxo completo.
- Relatório de testes e cobertura.
- Preparação para transição (handoff).

## Milestones e Critérios de Aceitação
| Marco | Data alvo | Critérios |
|-------|-----------|-----------|
| M1 — Planejamento aprovado | Fim da Semana 0 | Requisitos validados, arquitetura aprovada, repositório com artefatos deste pacote |
| M2 — Sprint 1 Demo | Fim da Semana 3 | CRUDs e inscrições funcionando, testes >=70% cobertura |
| M3 — Sprint 2 Demo | Fim da Semana 5 | Certificados automáticos, dashboard ativo, testes >=80% |
| M4 — Homologação OK | Semana 6 | Todos os bugs críticos resolvidos, checklist LGPD concluído |
| M5 — Entrega Final | Semana 7 | Documentação, vídeo, e release no GitHub |

## Dependências / Pré-Requisitos
- Aprovação dos requisitos e tecnologias pelo professor.
- Disponibilidade do projeto Supabase (chaves, quotas).
- Template visual do certificado (design + assinatura digital).
- Agenda de workshops reais (para testes com dados próximos ao real).

## Riscos do Cronograma
| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Atraso na aprovação inicial | Adia todas as fases | Manter professor atualizado semanalmente |
| Falta de tempo para certificados | Compromete Sprint 2 | Iniciar protótipo PDF logo após Sprint 1 |
| Dependência de Internet/Supabase | Bloqueia testes | Configurar ambiente local alternativo (Docker + Postgres) |
| Sobrecarga acadêmica | Reduz horas disponíveis | Replanejar tarefas com antecedência e focar no MVP |

## Próximas Ações
1. Registrar milestones no GitHub Projects.
2. Vincular requisitos (RF) a issues e aos marcos do cronograma.
3. Criar checklist de revisão por sprint (DoD/DoR) no board.
