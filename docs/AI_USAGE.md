# AI Usage Disclosure

AI-assisted tools were used during planning, implementation, testing, and code
review. The main uses were:

- discussing a manageable project scope and the division into Django
  applications;
- explaining Django ORM, migrations, forms, request flow, permissions, and
  transactions;
- suggesting and drafting parts of the Django test suite, including tests for
  validation, permissions, ownership, filters, and booking conflicts;
- helping with parts of the frontend, including Django templates, responsive
  CSS, and HTMX catalogue updates;
- reviewing the Docker and database setup and identifying useful verification
  commands.

Examples of questions and tasks given to the AI included:

- How should a small Django project with three roles and two resource types be
  divided into applications?
- Explain how a request moves through a Django URL, view, form, QuerySet, and
  template.
- Help create a responsive equipment catalogue using Django templates and CSS.
- How can HTMX update only the catalogue while keeping a normal GET fallback?
- Suggest tests for role permissions, booking ownership, invalid time ranges,
  and overlapping reservations.
- Explain the difference between a model, a `ModelForm`, `initial` values, and
  submitted `POST` data.
- Check whether the Docker Compose setup starts Django and PostgreSQL in the
  correct order.

AI suggestions were reviewed and adapted to the project structure. The final
behaviour was checked with Django system checks, migrations, automated tests,
coverage measurement, and manual browser testing.
