# AI Usage Disclosure

AI was used as a supporting tool during the planning and early development of CampusReserve. Its main uses were:

- brainstorming a project idea that matched the course requirements;
- discussing a simple Django architecture;
- explaining Django concepts such as projects, applications, models, ORM, and migrations;
- suggesting validation rules and test cases;
- providing example code that was reviewed as part of the learning process.

## Representative prompt summaries

- Suggest a manageable Django project with three roles, two filterable resource types, validated forms, tests, and Docker deployment.
- Explain how the folders and files in a basic Django project work and how an HTTP request reaches a template.
- Show a simple way to represent university rooms and individual equipment items as Django models, including basic validation and tests.

## Project decisions

The student selected Django and chose a server-rendered monolithic application instead of maintaining a separate frontend and REST API. The scope was kept intentionally small: study rooms, equipment, reservations, and three user roles. Development was divided into small stages so that each part could be reviewed and explained before continuing.

AI suggestions were not treated as authoritative. The project structure, scope, and code are reviewed during development, and automatic tests are used to verify implemented behaviour.
