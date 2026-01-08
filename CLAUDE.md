# Project Configuration for AI Assistants

## Project Overview

A fullstack web application template with FastAPI backend and Nuxt 3 frontend, designed for easy deployment as two separate services.

**Purpose**: Production-ready starting point for web applications with CRUD API, database integration, and modern frontend.

## Tech Stack

### Backend
- **Python 3.12+** - Language
- **FastAPI** - Web framework
- **SQLite / PostgreSQL** - Database (SQLite default for dev, PostgreSQL for production)
- **SQLAlchemy** - ORM (works with both databases)
- **Pydantic** - Validation and settings
- **uv** - Package manager

### Frontend
- **Nuxt 3** - Vue.js framework (SPA mode)
- **TypeScript** - Type safety
- **@nuxt/ui** - Tailwind CSS component library
- **Vite** - Build tool

## Architecture

### Two-Service Design
- **Backend** runs on port 8081, serves API endpoints
- **Frontend** runs on port 3000 (dev) or as static/server build
- **Development**: Frontend proxies `/api/*` to backend
- **Production**: Services deployed separately with CORS enabled

### Database Strategy
- **SQLite** (default): File-based, zero setup, perfect for development and simple apps
- **PostgreSQL**: Recommended for production with multiple instances or high concurrency
- Switch between them by changing `DATABASE_URL` environment variable

### CORS Configuration
- Backend reads `FRONTEND_URL` environment variable to allow cross-origin requests
- Critical for two-service deployment architecture

## Project Structure

```
backend/
  lib/
    __init__.py
    database.py          # Database connection, handles SQLite & PostgreSQL
    models.py            # SQLAlchemy models (example: Item)
    schemas.py           # Pydantic schemas for API validation
    api.py               # API routes (example: CRUD for items)
  scripts/               # Utility scripts
  main.py                # FastAPI app entry point, CORS setup
  pyproject.toml         # Python dependencies (psycopg2-binary is optional)
  .env.example           # Environment variable template

frontend/
  composables/
    useApi.ts            # API client composable (fetch wrapper)
  app.vue                # Main SPA component with example UI
  nuxt.config.ts         # Nuxt config (proxy, modules, settings)
  package.json           # Node dependencies

docs/
  adr/                   # Architecture Decision Records
DEPLOYMENT.md            # Deployment guide (platform-agnostic)
ENV_VARS.md              # Environment variable reference
README.md                # User-facing documentation
```

## Key Files Reference

### Backend Files
- **`backend/lib/database.py`** - Database setup, auto-creates tables
- **`backend/lib/models.py`** - Define SQLAlchemy models here
- **`backend/lib/schemas.py`** - Define Pydantic request/response schemas
- **`backend/lib/api.py`** - Define API endpoints (FastAPI routers)
- **`backend/main.py`** - Main app, CORS middleware, includes routers
- **`backend/.env`** - Local environment variables (not in git)

### Frontend Files
- **`frontend/app.vue`** - Main component, full app UI
- **`frontend/composables/useApi.ts`** - API calls to backend
- **`frontend/nuxt.config.ts`** - Nuxt configuration
- **`frontend/.env`** - Frontend environment variables (not in git)

## Environment Variables

### Backend (backend/.env)
- `DATABASE_URL` - Database connection (default: `sqlite:///./app.db`)
- `FRONTEND_URL` - Frontend URL for CORS (default: `http://localhost:3000`)

### Frontend (frontend/.env)
- `NUXT_PUBLIC_API_BASE_URL` - Backend API URL (default: `http://localhost:8081`)

**Note**: Frontend variables are baked into bundle at build time. See `ENV_VARS.md` for details.

## Development Setup

### Quick Start (SQLite - Zero Setup)
```bash
# Terminal 1 - Backend
cd backend
uv sync
cp .env.example .env
python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

Access: http://localhost:3000

### Using PostgreSQL Instead
```bash
# Install PostgreSQL driver
cd backend
uv pip install psycopg2-binary

# Update .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
```

## Common Tasks

### Adding a New Database Model
1. Edit `backend/lib/models.py` - Add new SQLAlchemy model class
2. Edit `backend/lib/schemas.py` - Add Pydantic schemas for validation
3. Edit `backend/lib/api.py` - Add API endpoints for the model
4. Edit `backend/main.py` - Include the new router if separate
5. Restart backend - Tables auto-create on startup

### Adding a New API Endpoint
1. Edit `backend/lib/api.py` - Add route with `@router.get/post/put/delete`
2. Use schemas from `schemas.py` for validation
3. Use `get_db()` dependency for database access
4. Return Pydantic models or dicts

### Modifying Frontend UI
1. Edit `frontend/app.vue` - Main component
2. Use composables from `frontend/composables/` for logic
3. Call backend via `useApi()` composable
4. Use `@nuxt/ui` components (UButton, UCard, etc.)

### Example: Extending the Items CRUD
The template includes a working "Items" model with full CRUD. To understand the pattern:
- Model: `backend/lib/models.py` (Item class)
- Schemas: `backend/lib/schemas.py` (ItemCreate, ItemResponse)
- API: `backend/lib/api.py` (5 endpoints: create, list, get, update, delete)
- Frontend: `frontend/app.vue` (full UI with modals, forms)

## Dependencies

### Backend
- **Core** (always needed): fastapi, uvicorn, sqlalchemy, pydantic, pydantic-settings
- **Optional**: psycopg2-binary (only for PostgreSQL)
- Install: `uv sync` (core) + `uv pip install psycopg2-binary` (if PostgreSQL)

### Frontend
- **Core**: nuxt, vue, @nuxt/ui
- Install: `npm install`

## Deployment

See `DEPLOYMENT.md` for comprehensive deployment guide including:
- Platform-agnostic instructions
- Docker examples
- Environment variable setup
- Database options
- Troubleshooting

See `ENV_VARS.md` for complete environment variable reference.

## Important Notes

- **No authentication** configured by default - add as needed
- **Database tables** auto-create on startup (no migrations needed for initial setup)
- **Frontend proxy** in development: `/api/*` → `http://localhost:8081`
- **SQLite limitations**: Single file, not ideal for multi-instance production
- **PostgreSQL benefits**: Concurrent access, better for production with multiple replicas
- **CORS**: Configured via `FRONTEND_URL` environment variable
- **API docs**: Auto-generated at `http://localhost:8081/docs` (Swagger UI)
