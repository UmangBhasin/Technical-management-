# Event Management System

Full-stack Event Management System with FastAPI backend and vanilla HTML/CSS/JavaScript frontend.

## Features

- JWT authentication
- Role-based access control (Admin and User)
- Admin-only maintenance module
- Membership module (add and update)
- Transactions module
- Reports module
- Frontend and backend validations
- Session handling on frontend via sessionStorage
- Secure password hashing using bcrypt

## Project Structure

```text
event-management-system/
  backend/
    requirements.txt
    app/
      __init__.py
      main.py
      core/
        config.py
        database.py
        security.py
        dependencies.py
      models/
        __init__.py
        user.py
        membership.py
        maintenance.py
        transaction.py
      schemas/
        __init__.py
        auth.py
        user.py
        membership.py
        maintenance.py
        transaction.py
        report.py
      routers/
        __init__.py
        auth.py
        users.py
        membership.py
        maintenance.py
        transactions.py
        reports.py
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

## Backend Setup (FastAPI)

1. Open terminal in backend directory:

```powershell
cd "g:\work\UMANG\project for placement\event-management-system\backend"
```

2. Create virtual environment:

```powershell
python -m venv .venv
```

3. Activate virtual environment:

```powershell
.\.venv\Scripts\activate
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Run FastAPI server:

```powershell
uvicorn app.main:app --reload
```

6. API will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## Frontend Setup (HTML/CSS/JS)

1. Open another terminal in frontend directory:

```powershell
cd "g:\work\UMANG\project for placement\event-management-system\frontend"
```

2. Serve frontend using Python HTTP server:

```powershell
python -m http.server 5500
```

3. Open browser:

- http://127.0.0.1:5500

## Default Admin Credentials

- Email: admin@events.com
- Password: Admin@123

Created automatically on first backend startup.

## API Summary

- Auth:
  - POST /api/auth/register
  - POST /api/auth/login
  - GET /api/auth/me
- Users:
  - GET /api/users/ (admin)
  - GET /api/users/profile
- Memberships:
  - POST /api/memberships/
  - GET /api/memberships/
  - PUT /api/memberships/{membership_id}
- Maintenance (admin):
  - POST /api/maintenance/
  - GET /api/maintenance/
  - PUT /api/maintenance/{record_id}
- Transactions:
  - POST /api/transactions/
  - GET /api/transactions/
  - PUT /api/transactions/{transaction_id}
- Reports:
  - GET /api/reports/dashboard
  - GET /api/reports/monthly-revenue (admin)

## Development Phases Recommended

1. Baseline completion (done): Auth + all modules + dashboards.
2. UI customization: colors, spacing, branding, typography.
3. Advanced business logic: filters, exports, pagination.
4. Deployment hardening: environment variables, production CORS, HTTPS.

## Production Notes

- Change SECRET_KEY in backend app/core/config.py before deployment.
- Replace SQLite with PostgreSQL for high-concurrency use.
- Restrict CORS origins in production.
- Add refresh tokens and token revocation for stronger session control.
