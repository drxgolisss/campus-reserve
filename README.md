# CampusReserve

CampusReserve is a student full-stack project for reserving university study rooms and equipment. The application is being built incrementally so that every part can be explained during the project review.

## Current state

Parts 1 and 2 provide:

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
- eleven automatic tests.

Authentication, roles, bookings, and HTMX updates will be added in later parts.

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
```

## Project structure

```text
campusreserve/  Django project configuration
core/           starter application and home page
resources/      room and equipment models, admin, seed command, and tests
templates/      shared HTML templates
static/         shared CSS and later JavaScript
docs/           proposal, lessons, requirements, and AI log
compose.yaml    web and PostgreSQL services
Dockerfile      reproducible web container image
manage.py       Django command-line entry point
```

## Configuration

Docker Compose includes safe development defaults. Copy `.env.example` to `.env` before changing local settings. Production secrets must never be committed to Git.
