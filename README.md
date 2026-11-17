# Snack Overflow

A production-minded office pantry tracker built for high concurrency, rock-solid data integrity, and delightful UX.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Vue 3](https://img.shields.io/badge/Vue-3.5+-4FC08D.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6+-3178C6.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

---

## 📹 Screen Recording Demo
> **Live Walkthrough**: [Watch the Video Demonstration](TODO: Replace with actual Loom or YouTube link)
>
> *(Covers: Authentication & RBAC, real-time pantry inventory, atomic snack consumption with concurrency recovery, interactive voting, admin modals, responsive mobile drawers, and error safety nets).*

---

## 🌐 Live Demo URLs (Render)
- **Frontend Web App**: `https://snackoverflow.onrender.com` *(or your custom domain)*
- **Backend API**: `https://snackoverflow-api.onrender.com`
- **Swagger Interactive API Docs**: `https://snackoverflow-api.onrender.com/docs`
- **Health Check**: `https://snackoverflow-api.onrender.com/health`

---

## 📐 Short Design Note

### Key Decisions
1. **Atomic Consumption via Row-Level Locks**: Rather than doing a prone-to-race `SELECT ... if quantity >= amount ... UPDATE`, the API executes a single atomic statement:
   ```sql
   UPDATE snacks 
   SET quantity = quantity - :amount, updated_at = NOW()
   WHERE id = :id AND quantity >= :amount 
   RETURNING id, name, category, quantity;
   ```
   PostgreSQL's default `READ COMMITTED` isolation serializes concurrent updates with exclusive row locks, guaranteeing inventory never dips below zero even if 50 users click "Consume" on the last packet simultaneously.
2. **Derived Snack Status (No Stored Status Column)**: Status (`stocked`, `running_low`, `gone`) is computed dynamically on read via a SQL `CASE` expression. This eliminates data synchronization anomalies where quantity changes but a status column remains stale.
3. **Database-Enforced Unique Constraints**: Duplicate voting prevention is delegated to PostgreSQL's composite unique index `UNIQUE (user_id, snack_id)`. Concurrent insertions trigger an `IntegrityError` (mapped cleanly to HTTP 409 `ALREADY_VOTED`), eliminating check-then-insert race conditions.
4. **Historical Snapshot in Activity Log**: `activities` stores a `snack_name` snapshot with `ON DELETE SET NULL`. If a snack is removed by an admin, the audit trail of past consumption and restocking remains intact.

### Trade-offs
- **PostgreSQL vs Redis for Real-Time Stock**: We chose pure PostgreSQL with row-level locks over an external Redis counter to preserve strict ACID transactions and avoid multi-database consistency overhead for a single-pantry scale.
- **Stateless JWTs in LocalStorage vs HttpOnly Cookie Sessions**: Storing JWTs in client storage simplifies cross-origin SPA communication and horizontal scaling without stateful session lookups, but sacrifices instantaneous server-side token revocation before expiry.
- **Sync SQLAlchemy 2.0 vs Async (asyncio)**: Sync engine with `psycopg 3` was chosen for predictable connection pooling, straightforward transaction rollbacks, and avoiding async ORM footguns, trading off extreme concurrent I/O throughput.

### What Would Break First at 100× the Users (10,000+ Active Users)?
1. **Single-Row Hotspot Contention**: When a popular snack is restocked, hundreds of concurrent requests contend for the same row lock (`UPDATE snacks WHERE id = :id`), exhausting DB connection pools.
   - *Mitigation*: Move real-time decrementing to an in-memory Redis cluster (`DECRBY`) and asynchronously flush durable inventory state to PostgreSQL.
2. **Database Connection Limits**: PostgreSQL spawns a dedicated process per connection; hundreds of web workers will quickly exhaust `max_connections`.
   - *Mitigation*: Introduce **PgBouncer** in transaction pooling mode between FastAPI workers and Postgres.
3. **Audit Log Table Bloat**: The `activities` table will accumulate millions of records, degrading history lookups and joins.
   - *Mitigation*: Implement declarative table partitioning by range on `created_at` (monthly partitions) and offload read-heavy analytics to replicas.
4. **Token Invalidation Gaps**: Stateless JWTs cannot be revoked immediately upon employee offboarding or role downgrade.
   - *Mitigation*: Introduce a Redis-backed token revocation list or switch to short-lived 5-minute access tokens paired with rotating HttpOnly refresh tokens.

---

## ✨ Features

### 📊 Dashboard (`/`)
- **Hero Overview**: Personalized greeting with live pantry status indicators.
- **Summary Metric Cards**: Animated count-up totals for **Stocked**, **Running Low**, **Gone**, and **Total Snacks**.
- **Snack of the Week**: Showcase spotlight highlighting the top-voted snack (deterministic tie-breaking by alphabetical name). Supports 1-click voting directly from the card.
- **Running Low Strip**: Fast-access horizontal scroll-snap strip to quickly restock or grab snacks that are about to run out.

### 🍪 Snack Catalog (`/snacks`)
- **Unified Single-Page Catalog**: Displays all snacks on a continuous, responsive grid with a live total count badge, removing friction from fragmented 1, 2, 3 page navigation.
- **Filter & Search Controls**:
  - Sticky category pills (**All**, **Sweet**, **Savoury**, **Drink**, **Healthy-ish**) that snap under the navbar.
  - Stock status dropdown (**All**, **Stocked**, **Running Low**, **Gone**).
  - Multi-criteria sorting (**Name**, **Quantity**, **Votes**, **Created Date**) with ASC/DESC order.
  - Debounced search query (300ms) with SQL wildcard escaping (`%` and `_`).
- **URL Query Param Two-Way Sync**: Filters and sorting reflect in browser URL (`?category=sweet&status=stocked&sort_by=votes&order=desc`) and persist across reloads.
- **Tactile Stepper & Consume**: Quantity stepper (`1` to `min(quantity, 10)`), inline submit spinner, checkmark success feedback, and live quantity countdown.
- **409 Concurrency Resilience**: Catches `INSUFFICIENT_STOCK` (409) if another user grabs the last item, animates a card shake, fires a toast (*"Someone beat you to it. Only X left"*), and re-syncs state.
- **Interactive Voting**: Toggle heart icon with micro-animations, immediate optimistic feedback, and conflict recovery against `ALREADY_VOTED` and `VOTE_NOT_FOUND`.
- **Status Visuals**: Amber warning badges for `running_low` snacks; desaturated grayscale with disabled consume controls for `gone` snacks.

### 🛡️ Admin Interface (Role-Gated)
- **Strict Role-Gating**: Admin controls (Add Snack FAB, card Edit, Restock, and Delete buttons) are rendered in the DOM only for `ADMIN` users. regular `MEMBER` users see clean consumer cards. All backend endpoints strictly enforce `require_admin`.
- **Add Snack Modal**: Form validating name, category, initial quantity, and low-stock threshold with inline server conflict handling (`SNACK_NAME_TAKEN`).
- **Edit Snack Modal**: Edit name, category, and threshold. Quantity is intentionally immutable here to prevent inventory tampering.
- **Restock Modal**: Inventory restock input with quick-add chips (`+5`, `+10`, `+20`) and an animated green glow pulse on completion.
- **Accessible Modals & Drawers**: ARIA `role="dialog"`, `aria-modal="true"`, focus trapping with Tab cycling, ESC key dismissal, scrollbar compensation, desktop centered dialogs, and mobile bottom drawers.

### 🎨 Design & UX
- **Royal Purple & White Theme**: Brand primary `#490982`, deep hover `#350661`, accent violet `#6816B3`, clean white `#FFFFFF`, and soft lavender surfaces `#F1E8F8`.
- **Adaptive Cross-Device Experience (Laptop & Mobile)**:
  - **Laptop/Desktop**: Full-scale edge-to-edge navigation bar, 4-column metric cards, pinned parallax hero animations, and rich 4-column footer.
  - **Mobile Phones (< 768px)**: Compact circular avatar header preventing title truncation, slide-out user drawer with navigation icons, 2x2 metric widget grid (Stocked, Low, Gone, Total), 2-row aligned filter & sort bar, and 44px touch targets.
- **GSAP Animations**: Micro-animations respecting `prefers-reduced-motion`.
- **Zero White Screens**: Global error boundary catches server outages, cold starts, and 404s with styled `<ErrorState>` and retry actions.

---

## 🛠️ Tech Stack

| Layer | Technologies | Justification |
|---|---|---|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0 (sync), psycopg 3 | Modern Python typing, automatic OpenAPI validation, high-performance C-extension Postgres driver |
| **Migrations** | Alembic | Version-controlled, reproducible database schema management |
| **Security** | Argon2-cffi, PyJWT, pydantic-settings | Memory-hard password hashing (Argon2id), cryptographically signed stateless tokens |
| **Database** | PostgreSQL 16 (in Docker) | ACID compliance, row-level locking, partial unique indexes, check constraints. Never SQLite. |
| **Frontend** | Vue 3 (Composition API, `<script setup>`), TypeScript | Reactive UI, strict type safety matching backend schemas |
| **State & Routing** | Pinia, Vue Router 4 | Centralized auth store, URL query sync, navigation guards |
| **Styling & Motion** | Pure CSS (CSS Tokens), GSAP, @fontsource (Baloo 2, Inter) | High-performance hardware-accelerated animations, zero external CSS framework bloat |
| **Containerization**| Docker, Docker Compose, Nginx Alpine | Multi-stage production build, non-root container security |

---

## 🚀 Quick Start (Docker — Recommended)

The simplest way to run the full stack (PostgreSQL, Backend API, and Frontend SPA):

### 1. Clone & Configure
```powershell
git clone https://github.com/dhanush200426/bipolar_task.git
cd bipolar_task
Copy-Item .env.example .env
```
*(By default, `.env.example` has `SEED_ON_START=true` to automatically populate demo users and snacks).*

### 2. Launch Containers
```powershell
docker compose up --build -d
```

### 3. Access Services
- **Frontend Web App**: [http://localhost](http://localhost) (Port 80)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### 4. Teardown
```powershell
docker compose down
# Or wipe database volumes:
docker compose down -v
```

---

## 💻 Manual Local Setup (Windows PowerShell)

If running directly without full Docker Compose:

### Prerequisites
- Python 3.12+
- Node.js 20+ (v22 recommended)
- Docker Desktop (for PostgreSQL container)

### Step 1: Database Setup
Start only the PostgreSQL container:
```powershell
cd D:\bipolar_task
docker compose up -d db
```

### Step 2: Backend Setup
```powershell
# 1. Create and activate virtual environment
python -m venv D:\bipolar_task\venv
& D:\bipolar_task\venv\Scripts\Activate.ps1

# 2. Install backend dependencies
cd D:\bipolar_task\backend
pip install -r requirements.txt

# 3. Configure environment
Copy-Item .env.example .env

# 4. Run migrations and seed data
alembic upgrade head
python scripts/seed.py

# 5. Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Frontend Setup
In a new terminal window:
```powershell
cd D:\bipolar_task\frontend\vue-project
Copy-Item .env.example .env
npm install
npm run dev
```
The frontend is available at [http://localhost:5173](http://localhost:5173).

---

## 🔐 Demo Credentials

| Role | Email | Password | Allowed Capabilities |
|---|---|---|---|
| **Admin** | `admin@snackoverflow.com` | `admin123` | Full access: Add snacks, edit metadata, restock inventory, delete snacks, consume, vote |
| **Member** | `member@snackoverflow.com` | `member123` | Pantry consumer: View catalog, consume snacks, vote/unvote, view dashboard |

*(Note: During local demo development, password verification accepts any password for existing emails for rapid testing, while hashing with Argon2 in production).*

---

## 🔑 Environment Variables Reference

### Root & Backend (`.env`)
| Variable | Default Value | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://snackoverflow:snackoverflow@localhost:5432/snackoverflow` | Normalized PostgreSQL connection string |
| `JWT_SECRET` | *(Random 32+ char hex string)* | Cryptographic key for signing JWT tokens |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Lifespan of access tokens |
| `CORS_ORIGINS` | `http://localhost,http://localhost:5173` | Comma-separated allowed browser origins |
| `ENV` | `development` | Environment mode (`development` / `production`) |
| `ENABLE_DOCS` | `true` | Enables `/docs` and `/redoc` OpenAPI interfaces |
| `SEED_ON_START` | `false` | When `true`, container startup automatically runs seed script |
| `PORT` | `8000` | Port for Uvicorn web server |

### Frontend (`frontend/vue-project/.env`)
| Variable | Default Value | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API base URL baked in at build time |

---

## 📡 API Reference Table

All endpoints are prefixed with the base URL. Protected routes require `Authorization: Bearer <token>`.

| Method | Path | Auth | Request Body | Success | Error Codes |
|---|---|---|---|---|---|
| `POST` | `/auth/login` | Public | `{ "email": str, "password": str }` | `200 OK` | `INVALID_CREDENTIALS` (401), `VALIDATION_ERROR` (422) |
| `GET` | `/auth/me` | Member / Admin | *None* | `200 OK` | `UNAUTHENTICATED` (401) |
| `GET` | `/health` | Public | *None* | `200 OK` | `SERVICE_UNAVAILABLE` (503) |
| `GET` | `/snacks/summary` | Member / Admin | *None* | `200 OK` | `UNAUTHENTICATED` (401) |
| `GET` | `/snacks` | Member / Admin | *Query Params: `category, status, q, page, page_size, sort_by, order`* | `200 OK` | `UNAUTHENTICATED` (401), `VALIDATION_ERROR` (422) |
| `GET` | `/snacks/{id}` | Member / Admin | *None* | `200 OK` | `SNACK_NOT_FOUND` (404), `UNAUTHENTICATED` (401) |
| `POST` | `/snacks` | **Admin Only** | `{ "name": str, "category": str, "quantity": int, "low_stock_threshold": int }` | `201 Created` | `FORBIDDEN` (403), `SNACK_NAME_TAKEN` (409), `VALIDATION_ERROR` (422) |
| `PATCH` | `/snacks/{id}` | **Admin Only** | `{ "name"?: str, "category"?: str, "low_stock_threshold"?: int }` | `200 OK` | `FORBIDDEN` (403), `SNACK_NOT_FOUND` (404), `SNACK_NAME_TAKEN` (409) |
| `DELETE`| `/snacks/{id}` | **Admin Only** | *None* | `204 No Content` | `FORBIDDEN` (403), `SNACK_NOT_FOUND` (404) |
| `POST` | `/snacks/{id}/consume` | Member / Admin | `{ "amount": int }` (1 - 100) | `200 OK` | `INSUFFICIENT_STOCK` (409), `SNACK_NOT_FOUND` (404), `VALIDATION_ERROR` (422) |
| `POST` | `/snacks/{id}/restock` | **Admin Only** | `{ "amount": int }` (1 - 10,000) | `200 OK` | `FORBIDDEN` (403), `SNACK_NOT_FOUND` (404), `VALIDATION_ERROR` (422) |
| `POST` | `/snacks/{id}/vote` | Member / Admin | *None* | `201 Created` | `ALREADY_VOTED` (409), `SNACK_NOT_FOUND` (404) |
| `DELETE`| `/snacks/{id}/vote` | Member / Admin | *None* | `200 OK` | `VOTE_NOT_FOUND` (404), `SNACK_NOT_FOUND` (404) |

---

## ⚠️ Consistent Error Format

The backend **never** returns HTML error pages or unhandled raw stack traces. All error responses conform to a strict JSON structure:

```json
{
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Someone beat you to it. Only 2 left."
  }
}
```

For Pydantic schema validation failures (HTTP 422), a descriptive `details` array is included:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed for: amount",
    "details": [
      {
        "type": "greater_than_equal",
        "loc": ["body", "amount"],
        "msg": "Input should be greater than or equal to 1",
        "input": 0
      }
    ]
  }
}
```

### Complete Error Code Enum
- `UNAUTHENTICATED` (401)
- `INVALID_CREDENTIALS` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` / `SNACK_NOT_FOUND` / `VOTE_NOT_FOUND` (404)
- `METHOD_NOT_ALLOWED` (405)
- `SNACK_NAME_TAKEN` / `ALREADY_VOTED` / `INSUFFICIENT_STOCK` (409)
- `VALIDATION_ERROR` (422)
- `SERVICE_UNAVAILABLE` (503)
- `INTERNAL_ERROR` (500)

---

## 🗄️ Database Architecture & Schema

PostgreSQL 16 is enforced with check constraints, foreign keys with explicit cascade policies, and functional unique indexes.

```
                    ┌───────────────────────────┐
                    │           users           │
                    ├───────────────────────────┤
                    │ id (PK, UUID)             │
                    │ name                      │
                    │ email (UQ, lowercase idx) │
                    │ password_hash (Argon2)    │
                    │ role (ADMIN, MEMBER)      │
                    │ created_at                │
                    └─────────────┬─────────────┘
                                  │ 1
                                  │
                  ┌───────────────┴───────────────┐
                  │ *                             │ *
        ┌─────────▼─────────┐           ┌─────────▼─────────┐
        │       votes       │           │    activities     │
        ├───────────────────┤           ├───────────────────┤
        │ id (PK, UUID)     │           │ id (PK, UUID)     │
        │ user_id (FK->usr) │           │ user_id (SET NULL)│
        │ snack_id (FK->snk)│           │ snack_id(SET NULL)│
        │ created_at        │           │ snack_name        │
        └─────────▲─────────┘           │ action            │
                  │ *                   │ amount            │
                  │                     │ created_at        │
                  │ 1                   └─────────▲─────────┘
        ┌─────────┴─────────┐                     │ *
        │      snacks       │                     │
        ├───────────────────┤                     │
        │ id (PK, UUID)     ├─────────────────────┘
        │ name (UQ, lower)  │
        │ category (ENUM)   │
        │ quantity (CHK >=0)│
        │ low_stock_thr (>=)│
        │ created_at        │
        │ updated_at        │
        └───────────────────┘
```

### Architectural Decisions & Justifications
1. **Derived Status (`status` is not a column)**:
   - Status (`stocked`, `running_low`, `gone`) is computed dynamically via SQL `CASE` expression on read:
     ```sql
     CASE 
       WHEN quantity = 0 THEN 'gone'
       WHEN quantity <= low_stock_threshold THEN 'running_low'
       ELSE 'stocked'
     END AS status
     ```
   - *Why*: Eliminates synchronization bugs where quantity changes but a status column remains stale.
2. **Activity Audit Log (`snack_name` snapshot & `ON DELETE SET NULL`)**:
   - `activities` stores a historical `snack_name` column snapshot. If an admin deletes a snack, the foreign key turns `NULL`, but historical logs still record what was consumed or restocked.
3. **Case-Insensitive Uniqueness**:
   - Unique index on `LOWER(name)` and `LOWER(email)` ensures `"Doritos"` and `"doritos"` cannot collide.
4. **Non-Negative Stock Constraint**:
   - `CHECK (quantity >= 0)` at the PostgreSQL database level acts as the final defense line against negative inventory.

---

## ⚡ Concurrency Control & Guarantees

### 1. Atomic Consumption (Zero Over-Consumption)
When multiple users try to consume the last item at the exact same millisecond, Snack Overflow uses a single atomic SQL statement with row-level locking:

```sql
UPDATE snacks
SET quantity = quantity - :amount,
    updated_at = NOW()
WHERE id = :id AND quantity >= :amount
RETURNING id, name, category, quantity, low_stock_threshold;
```

#### Why this is safe under concurrency:
- Under PostgreSQL default `READ COMMITTED` isolation, the `UPDATE` acquires an exclusive row-level lock (`RowExclusiveLock`).
- Subsequent concurrent transactions attempting to consume the same snack will wait for the first transaction to complete.
- When the second transaction acquires the lock, PostgreSQL re-evaluates the `WHERE` clause with the newly committed `quantity`.
- If the first transaction reduced `quantity` below `:amount`, the `WHERE quantity >= :amount` clause evaluates to `FALSE`. The statement updates 0 rows and returns `None`.
- The application catches this and returns a `409 Conflict` with `INSUFFICIENT_STOCK`.

#### Why standard SELECT-then-UPDATE is flawed:
```python
# BROKEN RACE CONDITION:
snack = db.query(Snack).filter(Snack.id == id).first()
if snack.quantity >= amount:
    # Gap where concurrent request can execute before commit!
    snack.quantity -= amount
    db.commit()
```
The naive approach has a Check-Then-Act race condition where both threads read `quantity = 1`, pass the check, and reduce the stock to `-1`.

### 2. One-Vote-Per-User Guarantee
The `votes` table has a composite unique constraint:
```sql
CONSTRAINT uq_user_snack UNIQUE (user_id, snack_id);
```
- A user cannot vote for the same snack twice.
- If concurrent vote requests arrive, the database constraint raises a PostgreSQL `UniqueViolation` (`IntegrityError`), caught cleanly and transformed into `409 ALREADY_VOTED`.
- Unvoting uses atomic `DELETE ... RETURNING id`. If 0 rows return, it yields `404 VOTE_NOT_FOUND`.

---

## 🧪 Testing Suite & Verification

The test suite runs against a real PostgreSQL database running in Docker (never SQLite, ensuring dialect-specific features like `RETURNING` and check constraints are verified).

### Running Tests
```powershell
& D:\bipolar_task\venv\Scripts\Activate.ps1
pytest -v
```

### Test Coverage Breakdown (45 Tests)
- `test_auth.py` (7 tests): Login success, password mismatch, timing attack dummy hash verification, valid/invalid/missing Bearer tokens, admin route protection against members.
- `test_consume_restock.py` (7 tests): Atomic consumption, insufficient stock 409 responses, gone status validation, restock incrementation, admin-only authorization.
- `test_errors.py` (10 tests): 404 unknown routes, 422 bad request bodies, 422 invalid query params, 401 unauthenticated, 403 forbidden, malformed JSON recovery, expired JWT tokens, negative amounts, SQL injection attempts, 404 on deleted snacks.
- `test_snacks.py` (13 tests): Full CRUD, duplicate name rejection, immutable quantity patch rejection, category filters, status filters, search wildcard escaping, pagination, multi-criteria sorting, summary metric counts, snack of the week alphabetical tie-breaking.
- `test_vote.py` (6 tests): Vote creation, duplicate vote prevention, non-existent snack voting, unvote success, unvote twice 404.
- `test_concurrency.py` (2 tests): Documented multi-threaded race simulation patterns.

### Frontend Type-Check & Build
```powershell
cd D:\bipolar_task\frontend\vue-project
npm run type-check   # Runs vue-tsc with zero TypeScript errors
npm run build-only   # Builds production bundle in dist/
```

---

## 📈 Design Note: 100x Scaling Analysis

If Snack Overflow scales from a small office pantry (100 users) to enterprise-wide adoption (10,000+ active users):

### 1. What Breaks First?
1. **Single-Row Lock Contention**:
   - When a popular snack is restocked, hundreds of concurrent requests attempt `UPDATE snacks WHERE id = :id`. PostgreSQL row locks serialize these transactions, leading to connection pool exhaustion and elevated request latencies.
   - *Mitigation*: Introduce Redis-backed distributed locks or write-behind decrement queues. A Redis `DECRBY` executes in memory in sub-millisecond time; once confirmed, background workers sync durable counts to PostgreSQL.
2. **Activity Table Bloat**:
   - With every consume and restock generating an `activities` entry, the table grows rapidly, degrading join queries.
   - *Mitigation*: Partition `activities` table by range on `created_at` (monthly partitions) and introduce read replicas for audit reporting.
3. **Stateless JWT Invalidation**:
   - Because tokens are stateless, an immediate role revocation or employee termination cannot invalidate an issued JWT until expiry.
   - *Mitigation*: Maintain a high-performance Redis token blocklist or use short-lived access tokens (5 minutes) with rotating refresh tokens stored in HTTP-only cookies.
4. **Database Connection Limits**:
   - PostgreSQL creates a backend process per connection. Hundreds of web worker processes can exceed `max_connections`.
   - *Mitigation*: Deploy **PgBouncer** in transaction pooling mode between the FastAPI instances and PostgreSQL.

---

## ☁️ Deployment Guide (Render)

Render is recommended for evaluation due to its free tier with Docker runtime and managed PostgreSQL.

### Step 1: Provision Managed PostgreSQL
1. Create a PostgreSQL instance on Render named `snackoverflow-db`.
2. Copy the **Internal Database URL**.
3. Note: The app automatically rewrites `postgres://` or `postgresql://` schemes into `postgresql+psycopg://` for SQLAlchemy 2.0.

### Step 2: Deploy Backend Web Service
1. Create a **Web Service** from repository with **Docker** environment.
2. Context: `./backend`, Dockerfile: `./backend/Dockerfile`.
3. Set environment variables:
   - `DATABASE_URL`: *(Your internal database URL)*
   - `JWT_SECRET`: *(32+ character hex string)*
   - `CORS_ORIGINS`: `https://snackoverflow.onrender.com`
   - `ENV`: `production`
   - `SEED_ON_START`: `true` (for initial startup)
   - `ENABLE_DOCS`: `true`

### Step 3: Deploy Frontend Static Site
1. Create a **Static Site** from repository.
2. Root Directory: `frontend/vue-project`.
3. Build Command: `npm run build-only`.
4. Publish Directory: `dist`.
5. Environment Variable: `VITE_API_BASE_URL` = `https://snackoverflow-api.onrender.com`.
6. Add SPA Rewrite Rule: `/*` -> `/index.html` (HTTP 200).

---

## 📁 Project Structure

```
D:\bipolar_task\
├── backend/
│   ├── alembic/              # Database schema migrations
│   │   ├── versions/         # Version-controlled migration files
│   │   └── env.py            # Migration runtime configuration
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py       # Auth dependencies (get_current_user, require_admin)
│   │   │   └── routes/       # API routers (auth.py, snacks.py)
│   │   ├── core/
│   │   │   ├── config.py     # Pydantic BaseSettings & connection normalizer
│   │   │   ├── db.py         # SQLAlchemy engine & session maker
│   │   │   ├── errors.py     # Global exception handlers & error codes
│   │   │   └── security.py   # Argon2 hashing & JWT encoding/decoding
│   │   ├── models/           # SQLAlchemy 2.0 ORM models (User, Snack, Vote, Activity)
│   │   ├── schemas/          # Pydantic v2 validation models
│   │   ├── services/         # Business logic (atomic consume, restock, status calculation)
│   │   └── main.py           # FastAPI entrypoint & middleware setup
│   ├── scripts/
│   │   └── seed.py           # Idempotent demo database seeder
│   ├── tests/                # Pytest test suite
│   ├── Dockerfile            # Python 3.12-slim non-root production image
│   └── requirements.txt      # Pinned dependencies
├── frontend/
│   └── vue-project/
│       ├── src/
│       │   ├── api/          # Axios HTTP client & typed service endpoints
│       │   ├── assets/       # Vector SVG illustrations
│       │   ├── components/   # Modals, snack cards, steppers, error states
│       │   ├── composables/  # Toast notifications & modal accessibility
│       │   ├── router/       # Vue Router navigation & auth guards
│       │   ├── stores/       # Pinia auth store with session persistence
│       │   ├── styles/       # CSS tokens (#490982 theme) & fluid typography
│       │   ├── views/        # Dashboard, Catalog, Login, 404, 403 views
│       │   └── App.vue       # Root component
│       ├── Dockerfile        # Multi-stage Node 22 build + Nginx Alpine
│       ├── nginx.conf        # Nginx SPA fallback configuration
│       └── package.json      # Frontend dependencies
├── docker-compose.yml        # Full-stack composition (Postgres, Backend, Frontend)
├── .env.example              # Template environment variables
└── README.md                 # Complete documentation
```

---

## ⚠️ Known Limitations
1. **Stateless JWT Tokens**: Logged-out tokens remain valid until expiration (default 60 minutes) as no central revocation blocklist is stored in this tier.
2. **Cold Starts on Render Free Tier**: Backend Web Service spins down after 15 minutes of inactivity; first load takes ~30-50s (mitigated by frontend skeleton states and error retry actions).
3. **Optimistic Voting UI**: Rapidly toggling votes in quick succession relies on sequential response arrival; rapid network disconnects require a refresh to synchronize.

---

## 📜 Changelog

- **Phase 1-4**: Core FastAPI foundation, PostgreSQL schema with Alembic, Argon2 authentication, and initial tests.
- **Phase 5-7**: Atomic consume endpoint with `UPDATE ... WHERE ... RETURNING`, one-vote guarantee, snack status calculation, and full CRUD.
- **Phase 8-10**: Vue 3 + TypeScript SPA, Pinia auth store, GSAP animated dashboard, and snack catalog with filter/sort/search URL sync.
- **Phase 11**: Accessible Admin Modals (Add, Edit, Restock, Delete) with focus trapping, ARIA roles, and mobile drawers.
- **Phase 12**: Complete Docker containerization (multi-stage frontend, non-root backend, healthchecks).
- **Phase 13**: Production deployment documentation, scheme normalization, and cloud hosting guide.
- **Phase 14**: Final verification audit, security hardening, robust error handling (DB outage 503, malformed JSON, SQL injection tests), comprehensive production documentation, and mobile-first responsive cross-device polish.
