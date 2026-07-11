# Logistic System API

Django REST API for managing logistics operations: authentication, orders, drivers, and delivery runs with stop-by-stop workflow.

---

## Features

- **JWT authentication** — login and token refresh (`manager`, `dispatcher`, `driver` roles)
- **Orders** — create/list orders with search and filters (`priority`, `status`)
- **Drivers** — list available drivers with search and filters
- **Build delivery run** — assign oldest open orders to an available driver (up to `max_stops`), sequence stops by priority
- **Run lifecycle** — start run → driver processes stops in sequence → complete run → cash bank
- **Stop workflow** — start (`en_route`), mark delivered, or fail (with required reason)
- **Role-based access** — managers/dispatchers manage runs; drivers act on their own runs/stops
- **Web UI** — login page and operations dashboard (stats, drivers list, build run)
- **Standardized API responses** — `{ success, message, data, error, status }`
- **Swagger docs** — interactive API documentation at `/swagger/`

### Delivery flow

1. Dispatcher/manager creates orders (`open`)
2. Build a run for an available driver (`POST /api/v1/delivery/build-run/`)
3. Start the run (`en_route`)
4. Driver starts each stop in sequence, then marks delivered or failed
5. Driver completes the run when all stops are finished
6. Manager/dispatcher marks the run cash-banked

---

## Setup instructions

### Prerequisites

- Python 3.10+
- pip / virtualenv

### 1. Clone and create a virtual environment

```bash
cd project
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Collect static files

```bash
python manage.py collectstatic
```

> Required in production to serve static files. In local `runserver` development, Django can serve files from `STATICFILES_DIRS` without this step.

### 6. Start the server

```bash
python manage.py runserver
```

---

## Web UI

| Page | URL | Description |
|------|-----|-------------|
| Login | [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) | Sign in with email/password; stores JWT tokens in `localStorage` |
| Dashboard | [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/) | Operations overview, driver list with status filter, and **Build run** |

Other useful URLs:

| Resource | URL |
|----------|-----|
| API base | `http://127.0.0.1:8000/api/v1/` |
| Swagger UI | `http://127.0.0.1:8000/swagger/` |
| Admin | `http://127.0.0.1:8000/admin/` |

### Auth header (API clients)

After login (UI or API), send:

```http
Authorization: Bearer <access_token>
```

---

## Demo credentials

| Role | Email | Password |
|------|-------|----------|
| Manager | `admin@gmail.com` | `1234` |
| Dispatcher | `dispatcher1@gmail.com` | `test@1234` |
| Driver | `driver1@gmail.com` | `test@1234` |

**API login example**

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "dispatcher1@gmail.com",
  "password": "test@1234"
}
```

Or open the web login page and use the same credentials.

---

## API overview

### Auth — `/api/v1/auth/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login/` | Obtain JWT access + refresh tokens |
| POST | `/refresh/` | Refresh access token |

### Dashboard API — `/api/v1/dashboard/` (manager / dispatcher)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard statistics |

### Orders — `/api/v1/order/` (manager / dispatcher)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List orders (`?search=`, `?priority=`, `?status=`) |
| POST | `/` | Create order |

### Delivery — `/api/v1/delivery/`

**Manager / Dispatcher**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/drivers/` | List drivers (`?status=`) |
| POST | `/build-run/` | Build run `{ "driver_id": <id> }` |
| GET | `/runs/` | List all runs |
| POST | `/runs/<id>/start/` | Start run (`en_route`) |
| PUT | `/runs/<id>/cash-banked/` | Mark run cash-banked |

**Driver**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/runs/driver/` | List my runs |
| GET | `/runs/driver/<id>/` | Run detail (with stops) |
| PUT | `/runs/driver/<id>/stops/<stop_id>/start/` | Start stop |
| PUT | `/runs/driver/<id>/stops/<stop_id>/delivered/` | Mark stop delivered |
| PUT | `/runs/driver/<id>/stops/<stop_id>/failed/` | Fail stop (body: `{ "failed_reason": "..." }`) |
| PUT | `/runs/driver/<id>/complete/` | Complete run |

---
