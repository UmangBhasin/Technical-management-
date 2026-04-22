# Event Management System

Full-stack Event Management System with a FastAPI backend and a vanilla HTML/CSS/JavaScript frontend.

## Features

- JWT authentication and role-aware authorization
- Roles: `admin` and `user`
- Admin-only maintenance module
- Membership module with add/update flows
- Transactions module with history
- Reports module (dashboard, users, memberships, transactions, monthly revenue)
- Frontend and backend validation
- Session state management on frontend storage
- Password hashing with bcrypt via Passlib

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, Pydantic, python-jose, passlib[bcrypt]
- Database: SQLite (default)
- Frontend: HTML, CSS, JavaScript (no framework)

## Project Structure

```text
event-management-system/
  backend/
    requirements.txt
    app/
      main.py
      api/
      core/
      models/
      schemas/
      routers/
      services/
  frontend/
    index.html
    login.html
    register.html
    admin-dashboard.html
    user-dashboard.html
    membership.html
    maintenance.html
    transactions.html
    reports.html
    css/
      styles.css
    js/
      config.js
      api.js
      common.js
      auth.js
      dashboard.js
      membership.js
      maintenance.js
      transactions.js
      reports.js
```

## Architecture Notes

- API routes are composed centrally in `backend/app/api/router.py`.
- Routers contain HTTP contract wiring and dependency injection.
- Service layer contains business rules and data operations.
- Schemas define contracts; models define persistent entities.

## Prerequisites

- Python 3.11+
- pip

## Quick Start (Windows)

From project root:

```powershell
cd "g:\work\UMANG\project for placement\event-management-system"
python -m venv "g:\work\UMANG\project for placement\.venv"
"g:\work\UMANG\project for placement\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
```

### Run Backend

```powershell
cd "g:\work\UMANG\project for placement\event-management-system\backend"
"g:\work\UMANG\project for placement\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
```

Backend URLs:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

### Run Frontend

In a second terminal:

```powershell
cd "g:\work\UMANG\project for placement\event-management-system\frontend"
"g:\work\UMANG\project for placement\.venv\Scripts\python.exe" -m http.server 5500
```

Frontend URL:

- `http://127.0.0.1:5500`

## Default Admin User

Seeded automatically on backend startup if not present:

- Email: `admin@events.com`
- Password: `Admin@123`

## API Summary

All API routes are under `/api`.

- Auth
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `GET /api/auth/me`
- Users
  - `GET /api/users/` (admin only)
  - `GET /api/users/profile`
- Memberships (admin only)
  - `POST /api/memberships/`
  - `GET /api/memberships/`
  - `GET /api/memberships/{membership_id}`
  - `PUT /api/memberships/{membership_id}`
- Maintenance (admin only)
  - `POST /api/maintenance/`
  - `GET /api/maintenance/`
  - `PUT /api/maintenance/{record_id}`
  - `GET /api/maintenance/users`
  - `POST /api/maintenance/users`
  - `PUT /api/maintenance/users/{user_id}`
  - `DELETE /api/maintenance/users/{user_id}`
- Transactions
  - `GET /api/transactions/memberships`
  - `POST /api/transactions/`
  - `GET /api/transactions/`
  - `PUT /api/transactions/{transaction_id}`
- Reports
  - `GET /api/reports/dashboard`
  - `GET /api/reports/monthly-revenue`
  - `GET /api/reports/users`
  - `GET /api/reports/memberships`
  - `GET /api/reports/transactions`

## Frontend Flow

- Public pages: `index.html`, `login.html`, `register.html`
- Authenticated pages:
  - Admin: dashboard, maintenance, membership, transactions, reports
  - User: dashboard, membership/view flows (where allowed), transactions, reports
- Shared navigation and route checks are handled in frontend JavaScript helpers.

## Production Notes

- Replace default `SECRET_KEY` in backend configuration.
- Restrict CORS origins from `*` to trusted domains.
- Move from SQLite to PostgreSQL for higher concurrency.
- Use HTTPS and secure cookie/session settings in deployment.

## Troubleshooting

- If backend fails to start, ensure dependencies are installed from `backend/requirements.txt`.
- If login fails unexpectedly, verify frontend points to `http://127.0.0.1:8000/api` and that backend is running.
- If port conflicts occur, free ports `8000` and `5500` or run on different ports.
