# ELLP Management System 

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](./README.pt-br.md)

## Sobre o Projeto

Este repositório destina-se ao desenvolvimento do projeto da disciplina **ESO71/IF66K - Oficina de Integração 2**, do curso de Engenharia de Software da UTFPR-CP.

O projeto está vinculado ao projeto de extensão **ELLP - Ensino Lúdico de Lógica e Programação** e tem como foco resolver uma demanda real da universidade.

### Ideia do Projeto: Controle de Oficinas

O objetivo deste sistema é criar uma plataforma para o gerenciamento completo das oficinas oferecidas pelo projeto ELLP. A plataforma centralizará o controle de todos os envolvidos e recursos, resolvendo os seguintes problemas:

* **Gerenciamento de Pessoas:** Cadastro e associação de Professores, Tutores e Alunos às oficinas.
* **Controle Acadêmico:** Definição e gerenciamento dos temas das oficinas.
* **Emissão de Certificados:** Geração e controle dos certificados de participação.

## Como executar o projeto completo

1. **Variáveis de ambiente**: copie `.env.example` para `.env` na raiz e em `backend/`, reutilizando os valores locais já presentes (Supabase local).
2. **Banco de dados (Supabase CLI)**: na raiz do repositório execute `supabase start`. O CLI sobe Postgres em `54322` e o gateway HTTP em `http://127.0.0.1:54321`.
3. **Backend (FastAPI)**:
	```bash
	cd backend
	python -m venv .venv && source .venv/bin/activate
	pip install -r requirements.txt
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
	```
4. **Frontend (Next.js)**:
	```bash
	cd frontend
	npm install
	npm run dev
	```
	As requisições serão encaminhadas para `http://localhost:8000` conforme definido em `.env`.
5. **Testes automatizados**:
	- Backend: `cd backend && pytest`
	- Frontend (E2E): `cd frontend && npx playwright install && npm run test:e2e`

## Participantes

* Matheus Mondaini Alegre de Miranda