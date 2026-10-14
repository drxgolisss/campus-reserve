# CampusReserve

CampusReserve is a Django web application for reserving university study rooms
and borrowable equipment.

## Current state

The application provides:

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
- room and equipment booking requests;
- overlap and availability validation;
- a personal booking list with edit and cancel actions;
- a manager queue with approve and reject actions;
- permission-protected resource creation and editing;
- automatic role setup in Docker;
- automated tests for resources, authentication, permissions, and bookings.

## Run with Docker

Requirements: Docker Desktop with Docker Compose.

```bash
docker compose up --build
```

Open <http://localhost:8000>.

Load demonstration users, resources, and bookings:

```bash
docker compose exec web python manage.py seed_demo
```

The development accounts use the password `CampusDemo2026!`:

- `student_demo` — Student;
- `manager_demo` — Manager;
- `admin_demo` — Administrator with Django Admin access.

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
docker compose exec web coverage run manage.py test
docker compose exec web coverage report
```

## Project structure

```text
campusreserve/  Django project configuration
accounts/       authentication tests, role definitions, and setup command
bookings/       booking models, forms, views, permissions, and tests
core/           home page
resources/      room and equipment models, admin, seed command, and tests
templates/      shared HTML templates
static/         shared CSS
docs/           proposal, screenshots, and AI usage disclosure
compose.yaml    web and PostgreSQL services
Dockerfile      reproducible web container image
manage.py       Django command-line entry point
```

## Configuration

Docker Compose includes safe development defaults. Copy `.env.example` to `.env` before changing local settings. Production secrets must never be committed to Git.

Password reset emails are printed in the web container logs during local
development. A real email provider can be configured when the application is
deployed.

The included passwords and development defaults are intended only for a local
course demonstration. They must be replaced before any public deployment.
