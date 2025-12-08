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

## Code Owners

* Matheus Mondaini Alegre de Miranda