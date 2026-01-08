# Fullstack Web Application Template

A modern fullstack web application template with FastAPI backend and Nuxt 3 frontend.

## Features

- **Backend**: FastAPI with SQLite/PostgreSQL and SQLAlchemy ORM
- **Frontend**: Nuxt 3 with Tailwind CSS and @nuxt/ui components
- **Type Safety**: Pydantic schemas for backend, TypeScript for frontend
- **Modern Build Tools**: uv for Python, npm for Node.js
- **Development Setup**: Automatic API proxying and hot reload

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite / PostgreSQL** - Database (SQLite default for development, PostgreSQL for production)
- **SQLAlchemy** - Python ORM
- **Pydantic** - Data validation and settings management
- **uv** - Fast Python package manager

### Frontend
- **Nuxt 3** - Vue.js framework with great DX
- **@nuxt/ui** - Tailwind CSS component library
- **TypeScript** - Type safety for frontend
- **Vite** - Fast build tool with HMR

## Prerequisites

- **Python 3.12+** - For backend
- **Node.js 18+** - For frontend
- **uv** - Python package manager (install with `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **PostgreSQL** (optional) - Only needed if you want to use PostgreSQL instead of SQLite

## Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies with uv
uv sync

# Configure environment
cp .env.example .env
# Edit .env and configure:
# - DATABASE_URL (default: SQLite, no setup needed)
# - FRONTEND_URL (for CORS, default: http://localhost:3000)

# The default configuration uses SQLite (no database server needed)
# For PostgreSQL, update DATABASE_URL and install: uv pip install psycopg2-binary
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Configure environment (optional for local dev)
cp .env.example .env
# Edit .env if you need to change the backend URL
# Default: NUXT_PUBLIC_API_BASE_URL=http://localhost:8081
```

## Running the Application

You need to run **both** the backend and frontend servers:

### Terminal 1 - Backend (FastAPI)

```bash
# From backend directory
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

Backend will be available at `http://localhost:8081`

### Terminal 2 - Frontend (Nuxt)

```bash
# From frontend directory
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Accessing the Application

**During development:**
- **Frontend**: http://localhost:3000 (Nuxt dev server with HMR)
- **Backend API**: http://localhost:8081 (proxied through Nuxt)
- **API Docs (Swagger)**: http://localhost:8081/docs
- **API Docs (ReDoc)**: http://localhost:8081/redoc

**Note:** The Nuxt dev server automatically proxies `/api/*` requests to the FastAPI backend on port 8081.

## Project Structure

```
vibe-template/
├── backend/              # FastAPI backend
│   ├── lib/             # Backend modules
│   │   ├── database.py  # Database configuration
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── api.py       # API endpoints
│   ├── scripts/         # Utility scripts
│   ├── main.py          # FastAPI application entry point
│   ├── pyproject.toml   # Python dependencies
│   └── .env.example     # Environment template
├── frontend/            # Nuxt 3 frontend
│   ├── composables/     # Vue composables
│   │   └── useApi.ts    # API client
│   ├── app.vue          # Main SPA component
│   ├── nuxt.config.ts   # Nuxt configuration
│   └── package.json     # Frontend dependencies
├── docs/
│   └── adr/             # Architecture Decision Records
├── .gitignore
└── README.md
```

## API Endpoints

### Items (Example CRUD)

- `POST /api/items/` - Create new item
- `GET /api/items/` - List all items
- `GET /api/items/{id}` - Get specific item
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item

## Development Notes

### Backend
- Database tables are created automatically on startup
- CORS is configured for development (localhost:3000)
- API documentation is auto-generated from Pydantic schemas
- Uses PostgreSQL for persistence

### Frontend
- Runs in SPA mode (no SSR)
- API requests are proxied to backend during development
- Composables provide reusable API logic
- @nuxt/ui provides pre-built Tailwind CSS components
- Auto-imports for components and composables

### Production Build

To build the frontend for production:

```bash
cd frontend
npm run generate
```

This creates static files in `frontend/.output/public/` that can be served by FastAPI or a static file server.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Environment variable configuration
- Production deployment guide (platform-agnostic)
- Docker/container examples
- Production build testing
- Troubleshooting common issues

## Extending the Template

This template provides a working example with a simple "Items" model. To adapt it to your needs:

1. **Models**: Update `backend/lib/models.py` with your database schema
2. **Schemas**: Update `backend/lib/schemas.py` with your API request/response schemas
3. **API Routes**: Update `backend/lib/api.py` with your endpoints
4. **Frontend**: Update `frontend/app.vue` and composables for your UI needs

## License

MIT
