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

## Code Owners

* Matheus Mondaini Alegre de Miranda