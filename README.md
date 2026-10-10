# FocusFlow: FastAPI & PostgreSQL Task Management Platform

A full-stack task management and productivity web application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The platform features role-based access control, secure JWT cookie-based session handling, database migrations via **Alembic**, and a responsive frontend interface powered by **Jinja2** templates and asynchronous JavaScript.

---

## Key Features

* **Authentication & Security**:
* User registration and login utilizing `bcrypt` password hashing.
* Stateful user sessions powered by HTTP-only JWT access tokens stored in browser cookies.
* Protected route middleware supporting both standard OAuth2 Bearer tokens and cookie fallback.


* **Task & Todo Management**:
* Full CRUD capabilities (Create, Read, Update, Delete) scoped to the authenticated user.
* Priority levels (1 to 5) to organize urgent versus low-priority items.
* Task completion toggling with visual progress styling.


* **Role-Based Access Control (RBAC)**:
* Default `user` accounts with isolated task ownership.
* Elevated `admin` accounts with global permissions to audit and delete tasks across all users.


* **Account Settings**:
* Self-service password updates with mandatory current password re-verification.
* Contact number updates.


* **Database Reliability**:
* Version-controlled schema migrations using Alembic.
* Relational mapping between users and tasks via SQLAlchemy foreign keys.



---

## Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend Framework** | FastAPI (Python 3.10+) |
| **Database & ORM** | PostgreSQL, SQLAlchemy 2.0, Alembic |
| **Security & Auth** | Passlib, Bcrypt, Python-JOSE (JWT) |
| **Frontend UI** | Jinja2 Templates, Bootstrap 4, Vanilla JS (`fetch` API) |
| **Server Engine** | Uvicorn (ASGI) |

---

## Project Structure

```text
├── alembic/              # Database migration environments and revisions
├── routers/              # Modular API & page route handlers
│   ├── admin.py          # Admin-only audit & deletion routes
│   ├── auth.py           # Registration, login, and JWT token issue
│   ├── todos.py          # User-scoped task CRUD and SSR views
│   └── users.py          # Password reset and profile settings
├── static/               # Client-side static assets
│   ├── css/              # Bootstrap and custom stylesheets
│   └── js/               # base.js (API client) and vendor libraries
├── templates/            # Jinja2 server-rendered HTML templates
│   ├── add-todo.html     # Task creation page
│   ├── edit-todo.html    # Task editing and completion page
│   ├── layout.html       # Base layout template
│   ├── login.html        # Authentication entry page
│   ├── register.html     # User registration form
│   └── todo.html         # Main dashboard and task list
├── alembic.ini           # Alembic migration configuration
├── database.py           # SQLAlchemy engine & session maker
├── main.py               # FastAPI application initialization
├── models.py             # Database schemas (Users, Todos)
└── requirements.txt      # Project dependencies

```

---

## Getting Started

### 1. Prerequisites

* Python 3.10+ installed
* PostgreSQL server installed and running locally

### 2. Clone and Setup Environment

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Database Configuration

Create a PostgreSQL database named `todo`. Ensure your connection string in `database.py` and `alembic.ini` matches your local credentials:

```text
postgresql+psycopg2://<username>:<password>@localhost/<dbname>

```

### 4. Run Migrations

Generate tables and apply schema revisions:

```bash
alembic upgrade head

```

### 5. Launch the Application

Run the local development server:

```bash
uvicorn main:app --reload

```

* **Application URL**: [http://localhost:8000](http://localhost:8000)
* **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Specifications**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Reference Summary

### Authentication (`/auth`)

* `POST /auth/` - Register a new user account.
* `POST /auth/token` - Authenticate credentials and receive an access token cookie.
* `GET /auth/login-page` - Render login interface.
* `GET /auth/register-page` - Render registration interface.

### Tasks (`/todos`)

* `GET /todos/` - Retrieve all tasks for the logged-in user.
* `POST /todos/todo` - Create a new task.
* `GET /todos/todo/{id}` - Fetch a specific task by ID.
* `PUT /todos/todo/{id}` - Update title, description, priority, or completion.
* `DELETE /todos/todo/{id}` - Remove a task.

### Admin Panel (`/admin`)

* `GET /admin/todo` - List all tasks across all users.
* `DELETE /admin/todo/{id}` - Force-delete any task.

### User Profile (`/user`)

* `GET /user/` - Fetch account profile details.
* `PUT /user/password` - Update account password.
* `PUT /user/phonenumber/{phone_number}` - Update phone number.
