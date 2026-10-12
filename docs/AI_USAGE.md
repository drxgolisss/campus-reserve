# AI Usage Disclosure

AI-assisted tools were used during the initial project setup as a supporting
resource. The main uses were:

- discussing a manageable project scope and Django architecture;
- explaining Django projects, applications, ORM, migrations, and request flow;
- checking the Docker and database setup;
- suggesting validation cases and automated test scenarios.

Representative questions included:

- How should a small Django project with three roles and two resource types be
  divided into applications?
- How does a request move through a Django URL, view, form, QuerySet, and
  template?
- Which validation and test cases are needed for the resource catalogues and
  authentication flow?

The suggestions were reviewed and adapted during implementation. Django, a
server-rendered monolith, custom CSS, and the limited room/equipment scope were
chosen to keep the project understandable and possible to complete within the
course deadline. Automated tests are used to verify the implemented behaviour.
