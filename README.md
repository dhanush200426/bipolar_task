# Snack Overflow

A production-minded office pantry tracker for managing snacks and inventory.

## Live Demo URLs (Placeholders)
- **Frontend Web App**: `https://snackoverflow.onrender.com` *(or your custom domain)*
- **Backend API**: `https://snackoverflow-api.onrender.com`
- **Swagger Interactive API Docs**: `https://snackoverflow-api.onrender.com/docs`
- **Health Check**: `https://snackoverflow-api.onrender.com/health`

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
- **Unified Single-Page Catalog**: Displays all snacks on a single continuous, responsive grid with live total count, eliminating friction from multi-page 1, 2, 3 navigation.
- **Floating Action Button (FAB)**: Safe-area-aware pulsing FAB providing "+ Add snack" for Admins (opens modal) and "Snack of the Week" shortcut for Members.
- **State Handling**: Shimmering skeleton cards during load, clear-filter empty state, and error recovery view.

### Admin Interface (Role-Gated)
- **Strict Role-Gating**: Admin controls (Add Snack FAB, card Edit, Restock, and Delete buttons) are rendered ONLY when `authStore.isAdmin` is true. For regular members, none of these controls exist in the DOM, and all administrative endpoints strictly enforce backend `require_admin` authorization.
- **Add Snack Modal**: Complete form for name, category, initial quantity, and low-stock threshold with client-side validation mirroring backend constraints and inline server error display (e.g. `SNACK_NAME_TAKEN`).
- **Edit Snack Modal**: Allows modifying name, category, and low-stock alert threshold ONLY. Quantity is intentionally excluded to enforce pantry inventory integrity and require Restock activities.
- **Restock Modal**: Inventory restock input (1 - 10,000 packets) with rapid selection chips (`+5`, `+10`, `+20`) and a green glow highlight animation on the restocked snack card.
- **Delete Confirmation Dialog**: Accessible, focus-trapped confirmation dialog with clear destructive styling, removal animation, toast notification, and graceful 404 handling if the snack was already removed.
- **List Consistency Guarantee**: Automatically refetches the current page after every creation, update, restock, or deletion. If deleting the last item on a page leaves it empty, automatically transitions to the previous page.
- **Universal Modal Accessibility & Mobile Drawers**: All modals feature `role="dialog"`, `aria-modal="true"`, focus trapping with Tab cycle, Escape key dismissal, backdrop dismissal, scrollbar compensation to eliminate body scroll jump, and adaptive responsive styling (centered dialogs on desktop, bottom sheet drawers on phones).

### Authentication
- JWT-based authentication with role-based access control (Admin/Member)
- Secure login with demo accounts for testing
- Session persistence with automatic token refresh
- Protected routes with redirect preservation

### Design & UX
- **Toven-Inspired Purple & White Palette**: Primary royal purple (`#490982`), deep hover purple (`#350661`), accent violet (`#6816B3`), and crisp pure white background (`#FFFFFF`) with lavender surfaces (`#F1E8F8`).
- **Full-Scale Edge-to-Edge Header & Footer**: Widescreen-optimized navigation bar and rich 4-column footer featuring office location, 24/7 hours, social media links (LinkedIn, GitHub, X, Instagram), and live pantry inventory status.
- **Unified Single-Page Catalog**: Frictionless browsing where all pantry snacks load continuously on a single page with a live count badge, eliminating segmented 1, 2, 3 page navigation.
- **Typography & Motion**: Self-hosted fonts (Baloo 2 for headings, Inter for body) and GSAP micro-animations with full `prefers-reduced-motion` accessibility support.
- **Accessibility**: WCAG AAA/AA contrast-safe typography, 44px minimum touch targets, and full modal focus trapping.
- **Global Error Safety Net**: Intercepts network disconnects and server cold-starts, rendering styled recovery states rather than blank white screens.

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

## Quick Start

### Option 1: Docker (Recommended — One Command)

Prerequisites:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

1. **Configure environment**
```powershell
# Copy the example environment file
Copy-Item .env.example .env
```
*(By default, `.env.example` is pre-configured with `SEED_ON_START=false`. Change to `SEED_ON_START=true` to automatically load sample demo snacks and users).*

2. **Build and start all services**
```powershell
docker compose up --build
```
*(Add `-d` to run in detached/background mode).*

3. **Access the application**
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:8000
- **Swagger Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

4. **Stop services**
```powershell
docker compose down
```
*(To wipe the database volume and reset: `docker compose down -v`)*

---

### Option 2: Manual Local Development (Virtualenv)

### Prerequisites
- Python 3.11 or 3.12
- Node.js 20+ (v22 recommended)
- Docker Desktop (for PostgreSQL container)

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
# In D:\bipolar_task\backend
Copy-Item .env.example .env
# Edit .env with your settings (at minimum, set JWT_SECRET to 32+ characters)
```

4. **Start PostgreSQL database**
```powershell
cd D:\bipolar_task
docker compose up -d db
```

5. **Run database migrations & seed**
```powershell
cd D:\bipolar_task\backend
& D:\bipolar_task\venv\Scripts\Activate.ps1
alembic upgrade head
python scripts/seed.py
```

6. **Run the API server**
```powershell
cd D:\bipolar_task\backend
& D:\bipolar_task\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Verify health**
```powershell
curl http://localhost:8000/health
# Expected: {"status":"ok"}
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
Copy-Item .env.example .env
# Default: VITE_API_BASE_URL=http://localhost:8000
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

---

## Production Deployment Guide

### Platform Recommendation: Render

| Platform | Free/Cheap Tier Status (Verified 2024–2026) | PostgreSQL Support | Verdict |
|----------|---------------------------------------------|--------------------|---------|
| **Render (Recommended)** | **750 free instance hours/month**, 100% free Static Sites with CDN & rewrite rules, free PostgreSQL instance (1GB, 256MB RAM, 30 days active). **No credit card required.** | Managed PostgreSQL with internal/external URLs, connection pooling. | **Best choice for intern evaluation & demo deployments.** Simplest single-dashboard setup with zero upfront cost. |
| **Railway** | Initial 30-day trial ($5 credit). Free tier limited to $1/month credit, which quickly runs out when hosting a persistent 24/7 Postgres database. | Plugin PostgreSQL service. | Requires ongoing billing or credit card to avoid abrupt container shutdowns. |
| **Fly.io** | Eliminated permanent free tier for new accounts (7-day trial). Requires credit card upfront upon signup. | Managed Postgres clusters start at $38/mo; tiny self-hosted instances require card. | High setup friction; not suitable for quick, credit-card-free intern evaluation. |

---

### Step 1: Provision Managed PostgreSQL on Render

1. Log in to [Render Dashboard](https://dashboard.render.com/) (sign up with GitHub).
2. Click **New +** > **PostgreSQL**.
3. Configure the database:
   - **Name**: `snackoverflow-db`
   - **Database**: `snackoverflow`
   - **User**: `snackoverflow`
   - **Region**: Choose the region closest to you (e.g., *Singapore*, *Frankfurt*, *Oregon*).
   - **Instance Type**: Select **Free** (1 GB storage, 256 MB RAM, 100 connections).
4. Click **Create Database**.
5. Once provisioned, locate the **Connections** panel:
   - Copy the **Internal Database URL** (e.g., `postgres://snackoverflow:password@dpg-...:5432/snackoverflow`).
   - *(Note: Use the Internal URL for services running inside Render for lowest latency and free internal bandwidth).*

> [!TIP]
> **Scheme Normalization**: Cloud providers supply `postgres://` or `postgresql://` URIs. SQLAlchemy 2.0 with the `psycopg 3` driver strictly requires the `postgresql+psycopg://` scheme. Both `backend/app/core/config.py` and `backend/alembic/env.py` automatically detect and normalize this on the fly.

---

### Step 2: Deploy Backend Web Service (Docker)

1. In Render Dashboard, click **New +** > **Web Service**.
2. Connect your GitHub repository (`bipolar_task`).
3. Configure the service:
   - **Name**: `snackoverflow-api`
   - **Region**: Same region as your database.
   - **Language / Runtime**: **Docker**
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Context**: `./backend`
   - **Instance Type**: **Free** (512 MB RAM, 0.1 vCPU).
4. Expand **Advanced Settings**:
   - **Health Check Path**: `/health` (Render continuously monitors this path; startup succeeds once it returns HTTP 200 `{"status":"ok"}`).
5. Add the **Environment Variables**:

| Variable | Recommended Production Value | Purpose |
|----------|------------------------------|---------|
| `DATABASE_URL` | *(Paste Internal Database URL from Step 1)* | Database connection (auto-normalized to `postgresql+psycopg://`) |
| `JWT_SECRET` | *(64-character random hex string)* | Secure JWT token signing. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `JWT_ALGORITHM` | `HS256` | Cryptographic algorithm for JWTs |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token validity lifespan |
| `CORS_ORIGINS` | `https://snackoverflow.onrender.com` | **Exact frontend URL** without trailing slash. Requests from unauthorized origins will be blocked. |
| `ENV` | `production` | Disables debug query logs in console |
| `ENABLE_DOCS` | `true` | Leaves `/docs` interactive Swagger UI accessible for reviewer testing |
| `SEED_ON_START` | `false` | Keep `false` after initial database seeding |

6. Click **Create Web Service**.
   - Render pulls the code, builds the `backend/Dockerfile`, runs pending Alembic migrations (`alembic upgrade head`), and launches Uvicorn dynamically bound to the platform's `$PORT`.

---

### Step 3: Seed Database & Rotate Passwords

#### Option A: One-Time Auto-Seed on Startup
1. In the Web Service settings, temporarily set environment variable:
   `SEED_ON_START=true`
2. Trigger **Manual Deploy** > **Deploy latest commit**.
3. During container startup, `scripts/seed.py` creates demo users (`admin@snackoverflow.com`, `member@snackoverflow.com`), initial snack inventory across all 4 categories, and sample votes.
4. Immediately change `SEED_ON_START=false` once startup completes to avoid re-running checks on future deploys.

#### Option B: Run Seed via Render Web Shell
1. Go to your `snackoverflow-api` service in Render.
2. Click the **Shell** tab in the sidebar (opens an in-browser bash terminal inside your container).
3. Execute:
   ```bash
   python scripts/seed.py
   ```

#### Rotating Passwords in Production
To specify custom secure passwords instead of default demo credentials, provide environment variables before seeding:
```env
SEED_ADMIN_PASSWORD=YourSuperSecureAdminPassword2026!
SEED_MEMBER_PASSWORD=YourSuperSecureMemberPassword2026!
```
Or reset a password directly at any time via the Render Shell using Python:
```python
python -c "
from app.core.db import SessionLocal
from app.models import User
from app.core.security import hash_password

db = SessionLocal()
admin = db.query(User).filter(User.email == 'admin@snackoverflow.com').first()
if admin:
    admin.password_hash = hash_password('NewRotatedPasswordHere123!')
    db.commit()
    print('Password rotated successfully')
db.close()
"
```

---

### Step 4: Deploy Frontend as a Static Site

Render Static Sites are **100% free forever**, hosted on a global fast CDN with zero sleep/spin-down delays and automated SSL.

1. In Render Dashboard, click **New +** > **Static Site**.
2. Connect your GitHub repository (`bipolar_task`).
3. Configure the static site:
   - **Name**: `snackoverflow`
   - **Branch**: `main`
   - **Root Directory**: `frontend/vue-project`
   - **Build Command**: `npm run build-only`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://snackoverflow-api.onrender.com` *(Your deployed backend URL from Step 2, no trailing slash)*
   - *(Note: Vite bakes this URL into the client bundle at build time).*
5. **Configure SPA Rewrite Rule** *(Critical for deep links & browser refresh)*:
   - Go to the **Redirects / Rewrites** tab in your static site dashboard.
   - Click **Add Rule**:
     - **Type**: `Rewrite`
     - **Source**: `/*`
     - **Destination**: `/index.html`
   - Click **Save Changes**.
   *(This ensures paths like `/snacks`, `/login`, or `/snacks?category=sweet` serve `index.html` so Vue Router handles them client-side rather than returning an Nginx 404).*
6. Click **Create Static Site**.

---

### Step 5: Production Hardening & Operational Behavior

#### 1. API Documentation Policy (`/docs`)
- **Reviewer Evaluation Policy**: For this intern assignment, `ENABLE_DOCS=true` is enabled by default so reviewers can test endpoints, payloads, and error responses live via Swagger UI.
- **Enterprise Hardening**: In restricted corporate deployments, set `ENABLE_DOCS=false` in the backend environment variables to disable `/docs`, `/redoc`, and `/openapi.json`.

#### 2. HTTPS & SSL Enforcement
- Render automatically provisions Let's Encrypt certificates and enforces HTTPS redirection on both Web Services and Static Sites.
- The frontend `VITE_API_BASE_URL` must use `https://` to prevent browser mixed-content blocking.

#### 3. Free-Tier Cold-Start Handling
- **Sleep Behavior**: On Render's free tier, backend instances spin down after 15 minutes of inactivity. When a new visitor accesses the app, the first backend request will take **30–50 seconds** to wake up the container.
- **Frontend Graceful Handling**:
  - The Vue frontend does not crash or display a blank white screen.
  - The snack grid displays shimmering skeleton loaders during the wait.
  - If a connection times out before the backend finishes booting, the global error handling renders a styled `<ErrorState>` component with an informative message (*"We can't reach the pantry server. Check your connection and try again."*) and a **Try Again** button.

---

### Post-Deployment Smoke-Test Checklist

Verify your production deployment manually by completing this step-by-step checklist:

- [ ] **1. Health Check**: Visit `https://<your-backend>.onrender.com/health` in browser or curl.
  - *Expected*: HTTP 200 with JSON `{"status":"ok"}`.
- [ ] **2. Swagger Docs**: Visit `https://<your-backend>.onrender.com/docs`.
  - *Expected*: Interactive Swagger UI displays all authentication, snack, and voting endpoints.
- [ ] **3. Frontend Landing**: Visit `https://<your-frontend>.onrender.com`.
  - *Expected*: Clean render of the Snack Overflow login view with custom typography and warm palette.
- [ ] **4. Member Login**: Log in with `member@snackoverflow.com` / `member123`.
  - *Expected*: Redirects to `/snacks` or `/`. Admin toolbar (Add Snack FAB, Edit, Restock, Delete) is **not** in DOM.
- [ ] **5. Consume Snack**: Click the quantity stepper and click **Consume**.
  - *Expected*: Loading spinner appears, checkmark confirmation morphs, and quantity decreases in real time.
- [ ] **6. Voting & Tie-Breaker**: Click the heart button on a snack card.
  - *Expected*: Heart animates to active state, vote count increments by 1.
- [ ] **7. Admin Login & Role Check**: Log out, then log in with `admin@snackoverflow.com` / `admin123`.
  - *Expected*: "+ Add Snack" Floating Action Button and card admin controls (Edit, Restock, Delete) become visible.
- [ ] **8. Restock Item**: Open Restock modal on a snack, click `+10`, and submit.
  - *Expected*: Snack quantity updates immediately with green glow highlight animation.
- [ ] **9. SPA Deep Link & Refresh**: Navigate to `https://<your-frontend>.onrender.com/snacks?category=sweet&status=stocked` and press **F5** (hard refresh).
  - *Expected*: Page reloads directly on the filtered view without 404 errors (verifying rewrite rule).
- [ ] **10. 404 Route Handling**: Navigate to `https://<your-frontend>.onrender.com/invalid-path`.
  - *Expected*: Styled 404 NotFound view with "Back to Pantry" button; no blank screen.
- [ ] **11. Browser Console Check**: Open Developer Tools (F12) > Console.
  - *Expected*: Zero CORS errors, zero unhandled promise rejections, zero mixed-content warnings.

---

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string (auto-normalized to `postgresql+psycopg://`) | `postgresql+psycopg://snackoverflow:snackoverflow@localhost:5432/snackoverflow` |
| `JWT_SECRET` | JWT signing key (min 32 chars) | *Required* |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `60` |
| `CORS_ORIGINS` | Comma-separated allowed origins (no trailing slash) | `http://localhost:5173` |
| `ENV` | Environment mode (`development` / `production`) | `development` |
| `ENABLE_DOCS` | Toggle `/docs` and `/redoc` Swagger OpenAPI docs | `true` |
| `SEED_ON_START` | Automatically run `seed.py` on container startup | `false` |
| `PORT` | Web server listening port (injected by cloud platforms) | `8000` |
| `POSTGRES_USER` | PostgreSQL user | `snackoverflow` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `snackoverflow` |
| `POSTGRES_DB` | PostgreSQL database name | `snackoverflow` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL (baked in at build time) | `http://localhost:8000` |

## Demo Accounts

The application includes demo accounts for testing:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@snackoverflow.com | admin123 |
| Member | member@snackoverflow.com | member123 |

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
