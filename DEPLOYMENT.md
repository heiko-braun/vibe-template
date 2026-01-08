# Deployment Guide

## Overview

This application is designed to be deployed as two separate services:
- **Frontend**: Nuxt.js application (can be static or server-rendered)
- **Backend**: FastAPI application

This separation allows for independent scaling, flexible hosting options, and better caching of static assets.

## Environment Variables

### Backend (.env)

Required environment variables for the backend:

```bash
# Database (required)
# SQLite (file-based, no server needed)
DATABASE_URL=sqlite:///./app.db

# PostgreSQL (recommended for production)
# DATABASE_URL=postgresql://user:password@host:port/database

# Frontend URL for CORS (required in production)
# Development: http://localhost:3000
# Production: https://yourdomain.com
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)

The frontend needs to know the backend API URL:

```bash
# Backend API URL (required)
# Development: http://localhost:8081
# Production: https://api.yourdomain.com
NUXT_PUBLIC_API_BASE_URL=http://localhost:8081
```

## Development Mode

In development, run both servers separately:

```bash
# Terminal 1: Backend (port 8081)
cd backend
uv sync
cp .env.example .env
# Edit .env with your DATABASE_URL
python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload

# Terminal 2: Frontend (port 3000)
cd frontend
npm install
cp .env.example .env
# Edit .env if needed (default should work for local development)
npm run dev
```

The frontend uses a Nuxt dev proxy to forward `/api/*` requests to `http://localhost:8081`.

## Production Deployment

### Prerequisites

- Database: SQLite (file-based) or PostgreSQL (server-based, recommended for production)
- Two hosting environments (e.g., separate containers, VMs, or platform services)
- Ability to set environment variables in your hosting platform
- SSL/TLS certificates for HTTPS (required for production)

### Backend Deployment

1. **Prepare the backend service**:
   - Ensure Python 3.12+ is available
   - Install dependencies: `pip install uv && uv sync`
   - For PostgreSQL: `uv pip install psycopg2-binary` (not needed for SQLite)

2. **Set environment variables**:
   ```bash
   # SQLite (simple, single-file database)
   DATABASE_URL=sqlite:///./app.db

   # PostgreSQL (recommended for production, multi-user apps)
   # DATABASE_URL=postgresql://user:password@host:port/database

   FRONTEND_URL=https://yourdomain.com
   PORT=8081  # or use your platform's port variable
   ```

3. **Start command**:
   ```bash
   cd backend && uv run uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Configure domain/URL** for your backend API (e.g., `api.yourdomain.com`)

### Frontend Deployment

1. **Set build-time environment variables**:
   ```bash
   NUXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
   ```
   **CRITICAL**: This must be set before/during the build process, as Nuxt bakes it into the JavaScript bundle.

2. **Build the application**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Start command** (for server-rendered mode):
   ```bash
   node .output/server/index.mjs
   ```

4. **Alternative: Static deployment**:
   ```bash
   npm run generate
   # Serve files from .output/public/ with any static file server
   ```

5. **Configure domain/URL** for your frontend (e.g., `yourdomain.com`)

**Important Notes**:
- The API URL must be HTTPS in production to avoid mixed content errors
- Frontend environment variables are baked into the bundle at build time
- After changing `NUXT_PUBLIC_API_BASE_URL`, you must rebuild (not just restart)
- Both services should use HTTPS in production

### Database Setup

**Option 1: SQLite (Simple)**
1. Set `DATABASE_URL=sqlite:///./app.db` in backend environment
2. Database file is created automatically on first startup
3. Tables are created automatically by SQLAlchemy

**Option 2: PostgreSQL (Production)**
1. **Provision a PostgreSQL database** in your hosting environment
2. **Set `DATABASE_URL`** to PostgreSQL connection string in backend service
3. **Install PostgreSQL driver**: `uv pip install psycopg2-binary`
4. The database will be automatically created if it doesn't exist
5. Tables are created automatically on first startup

**Note**: For production deployments with multiple instances or high concurrency, PostgreSQL is strongly recommended over SQLite.

## Production Build Testing (Local)

To test the production build locally:

```bash
# Build the frontend
cd frontend
export NUXT_PUBLIC_API_BASE_URL=http://localhost:8081
npm run generate

# The static files are in frontend/.output/public/
# Serve them with any static file server:
npx serve .output/public

# In another terminal, run the backend:
cd backend
export FRONTEND_URL=http://localhost:3000
python -m uvicorn main:app --host 0.0.0.0 --port 8081
```

## How It Works

### API URL Configuration

The frontend determines the backend URL using Nuxt's `runtimeConfig`:

```typescript
// nuxt.config.ts (not included in template, but how it works)
runtimeConfig: {
  public: {
    apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8081'
  }
}
```

- **Development**: Override via `.env` file
- **Production**: Set via platform environment variables during build

All API calls use the `useApi()` composable which reads from this config.

### CORS Configuration

The backend automatically configures CORS based on the `FRONTEND_URL` environment variable:

- **Development**: Allows `http://localhost:3000`
- **Production**: Allows the URL set in `FRONTEND_URL`

## Deployment Checklist

### Initial Setup
- [ ] Choose database: SQLite (simple) or PostgreSQL (production)
- [ ] If PostgreSQL: Provision database and install psycopg2-binary
- [ ] Deploy backend with DATABASE_URL and FRONTEND_URL environment variables
- [ ] Deploy frontend with NUXT_PUBLIC_API_BASE_URL environment variable (set during build)
- [ ] Configure SSL/TLS certificates for both services
- [ ] Test API connectivity from frontend
- [ ] Test CRUD operations
- [ ] Verify CORS is working correctly

### Updates
- [ ] Backend: Deploy new code, service restarts automatically
- [ ] Frontend: Rebuild with environment variables, then deploy
- [ ] Database migrations: Run manually if schema changes

## Troubleshooting

### Frontend can't connect to backend
- Check `NUXT_PUBLIC_API_BASE_URL` is set correctly during build
- Verify backend is running and accessible at the configured URL
- Check CORS configuration in `main.py`
- Verify `FRONTEND_URL` matches your frontend URL (without trailing slash)
- Check browser console for error messages

### Mixed content errors (HTTP vs HTTPS)
- **Symptom**: Browser blocks requests from HTTPS frontend to HTTP backend
  ```
  Mixed Content: The page at 'https://yourdomain.com/' was loaded over HTTPS,
  but requested an insecure resource 'http://api.yourdomain.com/api/items/'.
  ```
- **Cause**: `NUXT_PUBLIC_API_BASE_URL` is set to HTTP instead of HTTPS
- **Fix**:
  1. Update environment variable to use HTTPS: `NUXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com`
  2. Rebuild the frontend (this rebakes the JavaScript bundle)
  3. Deploy the new build
  4. Verify in browser console

### Database connection fails
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Check PostgreSQL instance is running and accessible from backend
- Ensure database credentials are correct
- Check firewall rules allow connection from backend to database

### CORS errors
- Verify `FRONTEND_URL` in backend matches your frontend domain exactly
- Check that both services are using HTTPS in production
- Ensure `allow_credentials=True` is set in CORS middleware
- Check browser console for specific CORS error messages
- Verify no trailing slashes in URL configurations

## Architecture Notes

This deployment uses a **separated frontend/backend** architecture:
- Frontend is served as static files (cost-effective, fast CDN delivery)
- Backend is a standalone API server
- Communication happens via HTTP API calls
- No authentication included by default (add as needed)

Benefits:
- Independent scaling of frontend and backend
- Better CDN caching for static assets
- Easier to change frontend framework if needed
- Flexible deployment options

## Platform-Specific Examples

### Container-Based Platforms (Docker, Kubernetes, etc.)

**Backend Dockerfile example**:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/ .
RUN pip install uv && uv sync
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
```

**Frontend Dockerfile example**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build
CMD ["node", ".output/server/index.mjs"]
```

### Platform-as-a-Service (Heroku, Render, Fly.io, Railway, etc.)

Most platforms support:
- Automatic builds from Git repositories
- Environment variable configuration via dashboard/CLI
- Custom start commands
- Automatic SSL/TLS certificate provisioning

Refer to your platform's documentation for specific deployment instructions.

## Alternative: Single Service Deployment

If you prefer to serve the frontend from FastAPI (single service):

1. Build the frontend: `cd frontend && npm run generate`
2. Update `main.py` to serve static files from `frontend/.output/public/`
3. Deploy only the backend with static file serving enabled
4. No need for separate frontend deployment or CORS configuration
5. Single URL for both frontend and backend
