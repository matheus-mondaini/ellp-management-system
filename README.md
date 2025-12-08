# ELLP Management System

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](./README.pt-br.md)

**A management system for the ELLP extension project — workshops, teachers, tutors, students, and certificate issuance.**

---

## Project overview

`ellp-management-system` is a web-based platform to manage the ELLP (Brazilian Playful Teaching of Logic and Programming extension program). The system centralizes records for workshops, instructors, tutors and students, supports scheduling and attendance, and generates participation certificates. Built for a real need at university (UTFPR), this project demonstrates integration of OOP, databases, web development, testing and software architecture principles.

## Key features

* Workshop management: Create workshops, topics, schedules, capacity and assignments
* Attendance and enrollment tracking per workshop and per student
* Certificate generation (PDF) with template and verification ID
* Volunteer history and term generation for volunteers
* Automated tests and CI for quality assurance

## Testing & evaluation

* Write unit and integration tests for core flows (registration, enrollment, certificate generation).
* Use issues to document sprint backlog; attach PRs to issues for traceability.

## Contribution & workflow

* Use GitHub Issues for backlog and sprint tasks.
* Two sprints (per course spec); open PRs with linked issues.
* Keep commits well-described (following conventional commit guidelines). Include test coverage for added features.

## Supabase setup

1. Create a Supabase project (free or pro) and keep its `<project-ref>` handy.
2. In **Project Settings → Database → Connection info**, generate a password for the `postgres` user (save it somewhere safe).
3. Copy `.env.example` to `.env` both in the repository root and inside `backend/`, then update:
	* `DATABASE_URL=postgresql+psycopg://postgres:<password>@db.<project-ref>.supabase.co:6543/postgres?sslmode=require`
	* `SUPABASE_URL=https://<project-ref>.supabase.co`
	* `SUPABASE_SERVICE_ROLE_KEY` and anon key values from **API settings**.
4. Apply the schema with `psql` (or the Supabase SQL editor):

	```bash
	psql "postgresql://postgres:<password>@db.<project-ref>.supabase.co:6543/postgres?sslmode=require" \
	  -f docs/schema_supabase.sql
	```

5. Run the backend with `uvicorn app.main:app --reload` (or `docker-compose up backend`). The new DB helper auto-enforces SSL for Supabase endpoints.

### Local Supabase via CLI

If you prefer to self-host Supabase locally during development:

1. Install the CLI (`brew install supabase/tap/supabase` on macOS, or `npm install supabase --save-dev`). A Docker-compatible runtime (Docker Desktop, Rancher Desktop, Podman, or OrbStack) must be running.
2. From the repo root, run `supabase init` once. This creates the `supabase/` directory with `config.toml` (already checked in) plus a `.temp/` folder that stays gitignored.
3. Start the stack with `supabase start`. The CLI launches Postgres (port `54322`), the API/auth gateway (`http://127.0.0.1:54321`), Studio (`http://127.0.0.1:54323`), and the mail catcher (`http://127.0.0.1:54324`). Use `supabase stop` to tear it down.
4. Run `supabase status` (or `supabase status -o json`) to grab the local anon/service role keys and connection strings. Point your `.env` files to:
	* `SUPABASE_URL=http://127.0.0.1:54321`
	* `SUPABASE_ANON_KEY=<local anon key from supabase status>`
	* `SUPABASE_SERVICE_ROLE_KEY=<local service role key from supabase status>`
	* `DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres`
5. (Optional) Use `supabase link --project-ref <production_ref>` so `supabase db diff/push` can compare your local schema to the hosted project. See the [Supabase local development guide](https://supabase.com/docs/guides/local-development) for advanced config and OAuth examples.

## Running the full stack locally

1. **Copy env files**: duplicate `.env.example` to `.env` in the repo root and in `backend/`, keeping the provided local Supabase values.
2. **Database**: from the repo root run `supabase start` (the `supabase/` folder already contains the config). This exposes Postgres on `54322` and the HTTP gateway on `http://127.0.0.1:54321`.
3. **Backend API**:
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
	The web app will proxy API calls to `http://localhost:8000` (from `.env`).
5. **Automated tests**:
	- Backend: `cd backend && pytest`
	- Frontend E2E: `cd frontend && npx playwright install && npm run test:e2e`

## Code Owners

* Matheus Mondaini Alegre de Miranda