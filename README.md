# Snack Overflow

A production-minded office pantry tracker for managing snacks and inventory.

## Screenshots

*(Screenshots to be added - showing the dashboard with summary cards, snack of the week showcase, and running low strip)*

## Features

### Dashboard
- **Hero Section**: Personalized greeting with floating garnish parallax animations
- **Summary Cards**: Real-time pantry overview with animated count-up numbers (Stocked, Running Low, Gone, Total)
- **Snack of the Week**: Sticky showcase section with pinned illustration, rotation/scale animations, and voting capability
- **Running Low Strip**: Horizontal scroll-snap row for quick access to low-stock items with swipe/arrow navigation

### Snack Catalog (/snacks)
- **Sticky Category Tabs**: Pins under top bar when scrolling past the header; horizontally scrollable on mobile with scroll-snap (All, Sweet, Savoury, Drink, Healthy-ish).
- **Filter & Search Controls**: Stock status dropdown (All, Stocked, Running low, Gone), debounced name search (300ms), and multi-criteria sort (name, quantity, votes in asc/desc).
- **URL Query Param Sync**: Full two-way mapping (`?category=&status=&q=&page=&sort_by=&order=`), preserving filters across refresh and browser history, with automatic fallback on malformed query values.
- **Stale Response Protection**: Request counter and `AbortController` cancellation prevent race conditions from typing.
- **Snack Card Grid**: Responsive grid layout (1 column mobile, 2-3 tablet, 3-4 desktop) with GSAP fade/slide entrance stagger.
- **Status Visuals**: Amber ribbon and pulsing badge for `running_low` snacks; muted/desaturated grayscale for `gone` snacks with disabled stepper and Consume button.
- **Tactile Consume Stepper**: Quantity stepper (`1` to `min(quantity, 10)`), loading spinner to prevent double-submit, checkmark success morph, and live quantity countdown.
- **Concurrency 409 Resilience**: Catches `INSUFFICIENT_STOCK` (409), shakes the card with CSS keyframe animation, alerts the user with a toast, and refreshes the card with the latest server data.
- **Interactive Voting**: Toggle heart with pop micro-interaction, live vote count sync, and conflict recovery against `ALREADY_VOTED` and `VOTE_NOT_FOUND`.
- **Pagination**: Numbered page selector with prev/next controls, disabled boundary states, count summary, and automatic smooth scroll to grid top.
- **Floating Action Button (FAB)**: Safe-area-aware pulsing FAB providing "+ Add snack" for Admins (opens modal) and "Snack of the Week" shortcut for Members.
- **State Handling**: Shimmering skeleton cards during load, clear-filter empty state, and error recovery view.

### Authentication
- JWT-based authentication with role-based access control (Admin/Member)
- Secure login with demo accounts for testing
- Session persistence with automatic token refresh
- Protected routes with redirect preservation

### Design & UX
- Warm food-themed color palette (tomato, chili, orange, golden, cream, peach)
- Self-hosted fonts (Baloo 2 for headings, Inter for body)
- GSAP + ScrollTrigger animations with reduced motion support
- Responsive design with mobile-first approach
- Accessible with WCAG-contrast-safe colors and 44px minimum touch targets
- Global error safety net to prevent white screens

## Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (sync)
- psycopg 3 (PostgreSQL driver)
- Alembic (database migrations)
- Pydantic v2
- pydantic-settings
- PyJWT (JWT authentication)
- argon2-cffi (password hashing)
- pytest + httpx (testing)

### Database
- PostgreSQL 16 (Docker)

### Frontend
- Vue 3
- TypeScript
- Vite
- Pinia (state management)
- Vue Router
- GSAP + ScrollTrigger (animations)
- @fontsource (self-hosted fonts: Baloo 2, Inter)

### Design Notes

**Authentication Token Storage**: The frontend stores JWT tokens in localStorage for simplicity. This is a trade-off:
- **localStorage**: Vulnerable to XSS attacks (malicious JS can read tokens)
- **httpOnly cookies**: More secure against XSS but require CSRF protection and are harder to implement with SPA refresh tokens

For a production app, consider httpOnly cookies with CSRF tokens, short-lived access tokens with refresh rotation, and Content Security Policy (CSP) headers to mitigate XSS.

## Quick Start (Windows PowerShell)

### Prerequisites
- Python 3.11 or 3.12
- Docker Desktop

### Backend Setup

1. **Create and activate virtual environment**
```powershell
python -m venv D:\bipolar_task\venv
& D:\bipolar_task\venv\Scripts\Activate.ps1
```
*If script execution is blocked, run: `Set-ExecutionPolicy -Scope Process Bypass`*

2. **Install dependencies**
```powershell
cd D:\bipolar_task\backend
pip install -r requirements.txt
```

3. **Configure environment variables**
```powershell
# Copy the example env file
Copy-Item .env.example .env
# Edit .env with your settings (at minimum, set JWT_SECRET to 32+ characters)
```

4. **Start PostgreSQL**
```powershell
cd D:\bipolar_task
docker compose up -d db
```

5. **Run the API**
```powershell
cd D:\bipolar_task\backend
& D:\bipolar_task\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Verify health**
```powershell
# In another terminal or browser
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

7. **Run database migrations**
```powershell
cd D:\bipolar_task\backend
& D:\bipolar_task\venv\Scripts\Activate.ps1
alembic upgrade head
```

### Frontend Setup

1. **Navigate to frontend directory**
```powershell
cd D:\bipolar_task\frontend\vue-project
```

2. **Install dependencies**
```powershell
npm install
```

3. **Configure environment variables**
```powershell
# Copy the example env file
Copy-Item .env.example .env
# Edit .env if needed (default: VITE_API_BASE_URL=http://localhost:8000)
```

4. **Run development server**
```powershell
npm run dev
```

The frontend will be available at http://localhost:5173

5. **Build for production**
```powershell
npm run build
```

6. **Type checking**
```powershell
npm run type-check
```

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://snackoverflow:snackoverflow@localhost:5432/snackoverflow` |
| `JWT_SECRET` | JWT signing key (min 32 chars) | *Required* |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `60` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173` |
| `ENV` | Environment mode | `development` |
| `POSTGRES_USER` | PostgreSQL user | `snackoverflow` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `snackoverflow` |
| `POSTGRES_DB` | PostgreSQL database name | `snackoverflow` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

## Demo Accounts

The application includes demo accounts for testing:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@snackoverflow.test | Any password |
| Member | member@snackoverflow.test | Any password |

**Note**: For demo purposes, any password works. In production, proper password validation would be enforced.

### Role Behavior

- **Admin**: Full access to all features including creating, updating, and deleting snacks, restocking inventory, and viewing all activity.
- **Member**: Can view snacks, consume items, vote for snacks, and view the dashboard. Cannot modify snack details or restock inventory.

The backend enforces role-based access control. The frontend conditionally renders admin-only controls based on the user's role, but the backend is the final authority.

## Error Response Format

All API errors return a consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message"
  }
}
```

For validation errors (422), a `details` array is included:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed for: field1, field2",
    "details": [
      {
        "type": "value_error",
        "loc": ["body", "field1"],
        "msg": "error message",
        "input": "provided value"
      }
    ]
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHENTICATED` | 401 | Missing, invalid, or expired authentication token |
| `FORBIDDEN` | 403 | User lacks permission for the requested action |
| `INVALID_CREDENTIALS` | 401 | Incorrect email or password |
| `SNACK_NOT_FOUND` | 404 | Snack does not exist |
| `SNACK_NAME_TAKEN` | 409 | Snack name already exists |
| `INSUFFICIENT_STOCK` | 400 | Not enough stock to consume |
| `ALREADY_VOTED` | 409 | User has already voted for this snack |
| `VOTE_NOT_FOUND` | 404 | Vote does not exist |
| `VALIDATION_ERROR` | 422 | Request body validation failed |
| `NOT_FOUND` | 404 | Resource not found |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not allowed for this endpoint |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Tokens are obtained via the `/auth/login` endpoint and must be included in the `Authorization` header for protected endpoints.

### Login

**POST** `/auth/login`

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "User Name",
    "email": "user@example.com",
    "role": "admin"
  }
}
```

### Using the Token

Include the token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### Get Current User

**GET** `/auth/me`

Requires authentication. Returns the current user's information.

### Security Notes

- Passwords are hashed using Argon2 (memory-hard algorithm)
- Email addresses are normalized to lowercase before lookup
- Same error message is returned for unknown email vs wrong password (prevents user enumeration)
- Dummy hash verification is performed for non-existent users to prevent timing attacks
- Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 60 minutes)
- User roles are loaded from the database on each request (not trusted from token)

## API Endpoints

### Authentication

| Method | Path | Auth | Request | Response | Status Codes |
|--------|------|------|---------|----------|--------------|
| POST | `/auth/login` | None | `{email, password}` | `{access_token, token_type, user}` | 200, 401 (INVALID_CREDENTIALS), 422 |
| GET | `/auth/me` | Bearer token | - | `{id, name, email, role}` | 200, 401 (UNAUTHENTICATED) |

### Snacks

| Method | Path | Auth | Request | Response | Status Codes |
|--------|------|------|---------|----------|--------------|
| GET | `/snacks/summary` | Any user | - | `{stocked, running_low, gone, total, snack_of_the_week}` | 200, 401 |
| GET | `/snacks` | Any user | Query: `category`, `status`, `q`, `page`, `page_size`, `sort_by`, `order` | `{items, total, page, page_size, pages}` | 200, 401, 422 |
| GET | `/snacks/{id}` | Any user | - | `{id, name, category, quantity, low_stock_threshold, status, vote_count, voted_by_me, created_at, updated_at}` | 200, 401, 404 (SNACK_NOT_FOUND), 422 |
| POST | `/snacks` | Admin | `{name, category, quantity, low_stock_threshold}` | Snack object | 201, 401, 403 (FORBIDDEN), 409 (SNACK_NAME_TAKEN), 422 |
| PATCH | `/snacks/{id}` | Admin | `{name?, category?, low_stock_threshold?}` | Snack object | 200, 401, 403, 404, 409, 422 |
| DELETE | `/snacks/{id}` | Admin | - | - | 204, 401, 403, 404 |
| POST | `/snacks/{id}/consume` | Any user | `{amount}` (1-100) | Snack object | 200, 401, 404 (SNACK_NOT_FOUND), 409 (INSUFFICIENT_STOCK), 422 |
| POST | `/snacks/{id}/restock` | Admin | `{amount}` (1-10000) | Snack object | 200, 401, 403, 404, 422 |
| POST | `/snacks/{id}/vote` | Any user | - | `{vote_count, voted_by_me}` | 201, 401, 404, 409 (ALREADY_VOTED) |
| DELETE | `/snacks/{id}/vote` | Any user | - | `{vote_count, voted_by_me}` | 200, 401, 404 (VOTE_NOT_FOUND) |

#### Query Parameters (GET /snacks)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | enum | - | Filter by category: `sweet`, `savoury`, `drink`, `healthy-ish` |
| `status` | enum | - | Filter by status: `stocked`, `running_low`, `gone` |
| `q` | string | - | Search by name (case-insensitive, wildcards escaped) |
| `page` | integer | 1 | Page number (>= 1) |
| `page_size` | integer | 12 | Items per page (1-50) |
| `sort_by` | enum | `name` | Sort field: `name`, `quantity`, `votes`, `created_at` |
| `order` | enum | `asc` | Sort order: `asc`, `desc` |

#### Snack Status (Derived)

Status is computed from `quantity` and `low_stock_threshold`:
- `gone`: quantity = 0
- `running_low`: 1 <= quantity <= low_stock_threshold
- `stocked`: quantity > low_stock_threshold

### Concurrency Handling

The consume operation uses a single atomic SQL UPDATE statement to handle concurrent requests safely:

```sql
UPDATE snacks
SET quantity = quantity - :amount, updated_at = now()
WHERE id = :id AND quantity >= :amount
RETURNING id, name, category, quantity, low_stock_threshold
```

**Why this is safe under concurrency:**
- The UPDATE takes a row-level lock on the snack row
- Under PostgreSQL's default READ COMMITTED isolation, concurrent UPDATEs re-evaluate the WHERE clause after acquiring the lock
- If two transactions try to consume the same item simultaneously, only those that pass the WHERE clause (quantity >= amount) will succeed
- The CHECK constraint (quantity >= 0) is the final safety net if something bypasses the WHERE clause

**Why SELECT-then-UPDATE is unsafe:**
```python
# BAD - race condition
snack = db.query(Snack).filter(Snack.id == id).first()
if snack.quantity >= amount:
    snack.quantity -= amount  # Another transaction could have changed quantity here
    db.commit()
```
This pattern has a race condition: between the SELECT and UPDATE, another transaction could consume the item, leading to negative quantities.

**Transaction pattern:**
All write operations (consume, restock, vote, unvote) use a clean transaction pattern:
```python
try:
    # Perform database operations
    db.commit()  # Single commit at the end
except Exception:
    db.rollback()  # Rollback on any exception
    raise
```
This ensures that if the activity insert fails, the stock change rolls back, maintaining consistency.

### One Vote Per Person

Voting relies on the UNIQUE constraint on (user_id, snack_id) to prevent duplicate votes:

```python
vote = Vote(user_id=user_id, snack_id=snack_id)
db.add(vote)
db.commit()  # Will raise IntegrityError if constraint violated
```

**Why not check-then-insert:**
```python
# BAD - race condition
existing = db.query(Vote).filter(...).first()
if not existing:
    vote = Vote(...)
    db.add(vote)  # Another transaction could have inserted here
    db.commit()
```
This pattern has a race condition where two concurrent requests could both see no existing vote and both insert.

**Unvote idempotency:**
DELETE with RETURNING checks if the vote existed before deleting, making it safe under concurrency:
```sql
DELETE FROM votes
WHERE user_id = :user_id AND snack_id = :snack_id
RETURNING id
```
If no row is returned, the vote didn't exist (404 VOTE_NOT_FOUND).

## Project Structure

```
D:\bipolar_task\
├── backend/
│   ├── app/
│   │   ├── api/          # API routes and dependencies
│   │   ├── core/         # Configuration, database, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI application entry
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test suite
│   └── requirements.txt  # Pinned dependencies
├── frontend/
│   └── vue-project/
│       ├── src/
│       │   ├── api/           # API client and typed endpoints
│       │   ├── assets/        # SVG illustrations
│       │   ├── components/    # Reusable Vue components (AppShell, Toast, ErrorState, etc.)
│       │   ├── composables/   # Vue composables (useToast)
│       │   ├── router/        # Vue Router configuration with guards
│       │   ├── stores/        # Pinia stores (auth)
│       │   ├── styles/        # CSS tokens and base styles
│       │   ├── utils/         # Utility functions (errorMessages, clickOutside)
│       │   ├── views/         # Page components (Login, Dashboard, Snacks, etc.)
│       │   ├── App.vue        # Root component
│       │   └── main.ts        # Application entry
│       ├── .env.example      # Environment variables template
│       ├── index.html        # HTML template with fallback
│       ├── package.json      # NPM dependencies
│       └── vite.config.ts    # Vite configuration
├── scripts/              # Development and concurrency test scripts
├── docker-compose.yml    # PostgreSQL service
└── README.md
```

## Database Schema

### users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | varchar (UUID) | PRIMARY KEY | Unique identifier |
| name | varchar | NOT NULL | User's full name |
| email | varchar | NOT NULL, UNIQUE (case-insensitive) | User's email address |
| password_hash | varchar | NOT NULL | Argon2-hashed password |
| role | enum (ADMIN, MEMBER) | NOT NULL, default MEMBER | User role for permissions |
| created_at | timestamptz | NOT NULL, default now() | Account creation timestamp |

**Indexes**: `ix_users_email_lower` (unique, on LOWER(email)) - ensures case-insensitive email uniqueness

**Justification**: Email uniqueness is enforced via a unique index on the lowercase version to prevent users like "test@example.com" and "Test@Example.com" from coexisting. Role enum allows simple authorization. Password is stored as a hash, never plaintext.

### snacks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | varchar (UUID) | PRIMARY KEY | Unique identifier |
| name | varchar | NOT NULL, UNIQUE (case-insensitive) | Snack name |
| category | enum (SWEET, SAVOURY, DRINK, HEALTHYISH) | NOT NULL | Snack category for filtering |
| quantity | integer | NOT NULL, default 0, CHECK >= 0 | Current stock quantity |
| low_stock_threshold | integer | NOT NULL, default 5, CHECK >= 0 | Threshold for low stock alerts |
| created_at | timestamptz | NOT NULL, default now() | Creation timestamp |
| updated_at | timestamptz | NOT NULL, default now(), on update now() | Last update timestamp |

**Indexes**: `ix_snacks_name_lower` (unique, on LOWER(name)) - case-insensitive name uniqueness; `ix_snacks_category` - for category filtering

**Check Constraints**: `check_quantity_non_negative` (quantity >= 0); `check_low_stock_threshold_non_negative` (low_stock_threshold >= 0)

**Justification**: Quantity cannot be negative (enforced by DB). Low stock threshold allows configurable alerts. Category enum standardizes classification. Case-insensitive name uniqueness prevents duplicate snacks with different capitalization. `updated_at` tracks when stock changes.

### votes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | varchar (UUID) | PRIMARY KEY | Unique identifier |
| user_id | varchar | NOT NULL, FK users(id) ON DELETE CASCADE | User who voted |
| snack_id | varchar | NOT NULL, FK snacks(id) ON DELETE CASCADE | Snack voted for |
| created_at | timestamptz | NOT NULL, default now() | Vote timestamp |

**Indexes**: `uq_user_snack` (UNIQUE on user_id, snack_id) - prevents duplicate votes; `ix_votes_snack_id` - for counting votes per snack

**Foreign Keys**: `votes_user_id_fkey` (CASCADE delete); `votes_snack_id_fkey` (CASCADE delete)

**Justification**: CASCADE delete ensures votes are removed when user or snack is deleted, maintaining referential integrity. Unique constraint prevents a user from voting for the same snack multiple times. Snack index enables efficient vote counting.

### activities

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | varchar (UUID) | PRIMARY KEY | Unique identifier |
| user_id | varchar | FK users(id) ON DELETE SET NULL | User who performed action (nullable) |
| snack_id | varchar | FK snacks(id) ON DELETE SET NULL | Related snack (nullable) |
| snack_name | varchar | NOT NULL | Snapshot of snack name (preserves history) |
| action | enum (RESTOCKED, CONSUMED) | NOT NULL | Action type |
| amount | integer | NOT NULL, CHECK > 0 | Quantity changed |
| created_at | timestamptz | NOT NULL, default now() | Activity timestamp |

**Indexes**: `ix_activities_created_at` - for chronological queries; `ix_activities_snack_id` - for snack history

**Check Constraints**: `check_amount_positive` (amount > 0)

**Foreign Keys**: `activities_user_id_fkey` (SET NULL delete); `activities_snack_id_fkey` (SET NULL delete)

**Justification**: `snack_name` snapshot preserves activity history even if the snack is deleted (SET NULL on snack_id). SET NULL on user_id preserves activity if user is deleted (audit trail). Amount must be positive (you can't restock/consume 0 or negative items). Action enum standardizes activity types. Indexes enable efficient activity feeds and snack history queries.

### Derived Status

The `status` of a snack is **not stored** in the database. It is derived from `quantity` and `low_stock_threshold`:

- **gone**: quantity = 0
- **running_low**: 1 <= quantity <= low_stock_threshold
- **stocked**: quantity > low_stock_threshold

This is implemented via:
- SQL CASE expression in `app/services/snack_status.py::get_snack_status_case_expression()` for database queries
- Python function in `app/services/snack_status.py::get_snack_status()` for API responses

**Justification**: Derived status avoids data inconsistency (status could become out of sync with quantity). Computing it on read is cheap and always accurate.
