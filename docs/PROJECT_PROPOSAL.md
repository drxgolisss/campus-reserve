# CampusReserve — Project Proposal

**Author:** [Your name and surname]  
**Course:** [Course name]  
**Submission date:** 15 October 2026

## 1. Project idea

CampusReserve is a web application for reserving university study rooms and borrowable equipment. It solves a common problem: students often do not know which resources are available, while staff members need a simple way to manage resources and reservation requests.

The application will keep the scope intentionally small. It will support two types of resources, a clear reservation workflow, and three user roles. It will not include payments, real-time chat, push notifications, or integration with an external university system.

## 2. Project goals

The main goals are to:

- give authenticated students one place to find rooms and equipment;
- provide useful filters without reloading the whole page;
- prevent invalid and overlapping reservations;
- allow managers to maintain resources and process requests;
- allow administrators to manage users and permissions;
- provide a responsive interface for desktop and smartphone screens.

## 3. User roles

### Student

- log in and reset a forgotten password;
- browse and filter study rooms and equipment;
- create a reservation request;
- view their own requests;
- edit or cancel their own pending requests.

### Manager

- perform all student actions;
- add, edit, activate, and deactivate rooms and equipment;
- view reservation requests;
- approve or reject pending requests.

### Administrator

- access the Django administration panel;
- manage user accounts;
- assign and remove roles;
- manage all application records when necessary.

## 4. Main functional requirements

The application will provide:

1. authentication, logout, and password reset;
2. authorization based on three roles;
3. protected pages available only to authenticated users;
4. a filterable study-room catalogue;
5. a filterable equipment catalogue;
6. creation and modification of reservation records;
7. server-side validation of every submitted form;
8. asynchronous catalogue filtering using HTMX;
9. management pages protected by role permissions;
10. clear validation and authorization error messages.

## 5. Business rules

- A reservation start time must be earlier than its end time.
- A resource must be active before it can be reserved.
- A resource cannot have two overlapping active reservations.
- Pending and approved reservations block the selected time period.
- A student may view only their own reservations.
- A student may edit or cancel only their own pending reservation.
- Only a manager or administrator may approve or reject a request.

These rules make the problem well specified and provide testable domain logic.

## 6. Planned data model

The main entities will be:

- `User` — authentication data and role membership;
- `StudyRoom` — name, building, capacity, description, and active status;
- `EquipmentItem` — name, category, inventory code, condition, location, and active status;
- `RoomBooking` — student, room, start, end, status, and comment;
- `EquipmentBooking` — student, equipment item, start, end, status, and comment.

Reservation statuses will be `pending`, `approved`, `rejected`, and `cancelled`.

## 7. Data flow

1. A user sends a request from a browser.
2. Django checks authentication and role permissions.
3. A view validates the submitted form or filter parameters.
4. Domain logic checks availability and reservation rules.
5. Django reads or writes data in PostgreSQL.
6. The server returns a complete HTML page or an HTMX partial update.

```text
Browser -> Django view -> form and domain validation -> PostgreSQL
   ^                                                     |
   +------------ HTML or HTMX response -----------------+
```

## 8. Technology and architecture

The project will use a server-rendered monolithic architecture:

- Python and Django for backend logic, authentication, forms, and templates;
- PostgreSQL for persistent data;
- Bootstrap for visual design and responsive layout;
- HTMX for asynchronous filtering and partial page updates;
- pytest or Django's test framework for automated tests;
- coverage.py for code coverage measurement;
- Docker Compose for repeatable deployment;
- Git for source control and development history.

The source code will be divided into the `accounts`, `resources`, and `bookings` Django applications. Business rules will be kept outside HTML templates so that they can be tested independently.

## 9. Quality plan

The application will be checked at desktop and smartphone resolutions. Automated tests will cover models, forms, permissions, filters, reservation conflicts, and the main request workflows. The target is at least 75% code coverage, providing a safety margin above the required 70%.

All secrets and environment-specific settings will be passed through environment variables. The repository will contain example configuration, test data, setup instructions, and a visible history of incremental development.

## 10. Deployment and documentation

The final project will include:

- Docker configuration for the web application and database;
- instructions for starting the project on another computer;
- source code and database migrations;
- a short report containing the idea, architecture, data flow, and screenshots;
- an AI usage log describing the prompts and how the results were reviewed;
- sample accounts or a data-loading command for the demonstration.

## 11. Implementation schedule

- **9–10 October:** proposal and requirements review;
- **10–11 October:** repository, Docker, database, and base Django project;
- **11–12 October:** data model and sample data;
- **12–13 October:** authentication, password reset, roles, and permissions;
- **13–14 October:** room and equipment catalogues;
- **14–15 October:** HTMX filters and first reservation workflow;
- **16–17 October:** manager workflow and complete CRUD operations;
- **18 October:** responsive design and usability improvements;
- **19–20 October:** automated tests and coverage improvements;
- **21 October:** deployment check, report, screenshots, and presentation practice;
- **22 October:** final buffer and presentation.

## 12. Expected result

The final result will be a small but complete full-stack application that demonstrates database modelling, authentication, role-based authorization, validated CRUD operations, asynchronous interaction, automated testing, responsive design, version control, and containerized deployment.
