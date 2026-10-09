# AI Usage Log

This document records material AI assistance used during the CampusReserve project. AI is treated as a development assistant. Suggested decisions and generated code are reviewed, run, and tested by the student before being included in the project.

The log should remain accurate. New entries are added when AI materially influences architecture, implementation, testing, debugging, or documentation.

## Entry 1 — Project idea and architecture

**Date:** 9 October 2026  
**Tool:** OpenAI Codex  
**Purpose:** Select a manageable project idea and map it to the assignment requirements.

**Prompt:**

> Help me plan a simple third-year full-stack student project with Django. It must include login and password reset, three roles, protected resources, two filterable item tables, responsive design, validated forms, CRUD operations, AJAX or a similar technique, Git history, Docker deployment, automated tests with at least 70% coverage, and a short report. Propose an architecture and a two-week implementation plan that a full-stack beginner can understand.

**How the result was used:**

- The CampusReserve topic was selected from the planning discussion.
- The suggested scope was reduced to rooms, equipment, and reservations.
- The architecture was adapted to use server-rendered Django, Bootstrap, HTMX, and PostgreSQL.
- The schedule was adjusted to the proposal and final-presentation deadlines.

**Student verification:**

- The proposed features were compared with the assignment requirements.
- Unnecessary features such as payments and real-time chat were excluded.
- The final proposal will be reviewed and edited before submission.

## Entry 2 — Django project foundation

**Date:** 9 October 2026  
**Tool:** OpenAI Codex  
**Purpose:** Create a small, beginner-readable Django foundation that can be run and tested before domain features are added.

**Prompt:**

> Create the first incremental part of CampusReserve using Django, PostgreSQL, and Docker Compose. Include environment-based settings, one simple responsive page, a smoke test, clear run instructions, and an explanation of project, app, URL, view, template, and migration concepts. Do not implement bookings or roles yet.

**How the result was used:**

- The base Django project and `core` application were created.
- Docker Compose was configured with a PostgreSQL service.
- A responsive starter page and shared stylesheet were added.
- A smoke test and beginner lesson were included.

**Automated verification:**

- Python source files compiled successfully.
- Django migrations completed successfully in the local test environment.
- `manage.py check` reported no issues.
- The automatic test passed.
- The home page returned HTTP status 200.
- Docker Compose accepted the configuration; the image build remains to be repeated while Docker Desktop is running.

**Student follow-up:**

- Read `LESSON_01_FOUNDATION.md`.
- Reproduce the run and test commands.
- Explain the request path from URL to template in their own words.

## Entry template

### Entry [number] — [short task name]

**Date:** [date]  
**Tool:** [tool name]  
**Purpose:** [what assistance was requested]

**Prompt:**

> [prompt used]

**How the result was used:**

- [accepted, changed, or rejected suggestion]
- [files or project areas affected]

**Student verification:**

- [commands, tests, documentation, or manual checks performed]
- [what the student changed after reviewing the answer]

## Suitable future uses

Future entries may cover real tasks such as:

- explaining Django groups and permissions;
- reviewing the reservation data model;
- suggesting edge cases for form validation;
- proposing tests for overlapping reservations;
- explaining an error message during debugging;
- reviewing documentation for missing setup steps.

These should only be logged after the corresponding assistance is actually used.
