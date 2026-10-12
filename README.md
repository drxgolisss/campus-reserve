# CampusReserve

CampusReserve is a student full-stack project for reserving university study rooms and equipment. The application is being built incrementally so that every part can be explained during the project review.

## Current state

The current version provides:

- a minimal Django project;
- a starter `core` application;
- a responsive home page;
- PostgreSQL in Docker Compose;
- environment-based configuration;
- `StudyRoom` and `EquipmentItem` database models;
- an initial resources migration;
- resource management in Django Admin;
- a repeatable demonstration-data command;
- room and equipment catalogue pages;
- validated search and filter forms;
- HTMX catalogue updates with a normal GET fallback;
- login, logout, and password reset;
- protected resource catalogues;
- Student, Manager, and Administrator roles;
- automatic role setup in Docker;
- automated tests for resources, authentication, and permissions.

The reservation workflow will be added in the next part.

## Run with Docker

Requirements: Docker Desktop with Docker Compose.

```bash
docker compose up --build
```

Open <http://localhost:8000>.

To stop the containers:

```bash
docker compose down
```

To remove the development database as well:

```bash
docker compose down --volumes
```

The last command deletes local development data, so it should only be used when a fresh database is intended.

## Useful checks

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py setup_roles
```

## Project structure

```text
campusreserve/  Django project configuration
accounts/       authentication tests, role definitions, and setup command
core/           home page
resources/      room and equipment models, admin, seed command, and tests
templates/      shared HTML templates
static/         shared CSS and later JavaScript
docs/           proposal, requirements checklist, and AI usage disclosure
compose.yaml    web and PostgreSQL services
Dockerfile      reproducible web container image
manage.py       Django command-line entry point
```

## Configuration

Docker Compose includes safe development defaults. Copy `.env.example` to `.env` before changing local settings. Production secrets must never be committed to Git.

Password reset emails are printed in the web container logs during local
development. A real email provider can be configured when the application is
deployed.
