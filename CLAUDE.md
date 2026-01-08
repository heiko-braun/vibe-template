# Project Configuration

## Project Overview

A fullstack web application template built with FastAPI (backend) and Nuxt 3 (frontend).

## Tech Stack

### Backend
- Python 3.12+
- FastAPI web framework
- PostgreSQL database
- SQLAlchemy ORM
- uv for package management

### Frontend
- Nuxt 3 (Vue.js framework)
- TypeScript
- @nuxt/ui (Tailwind CSS components)
- Vite build tool

## Project Structure

```
backend/         # FastAPI backend
  lib/          # Backend modules (models, database, api)
  scripts/      # Utility scripts
  main.py       # Application entry point

frontend/       # Nuxt 3 frontend
  composables/  # Vue composables
  app.vue       # Main SPA component

docs/adr/       # Architecture Decision Records
```

## Development Setup

**Backend**: Run from `backend/` directory with `python -m uvicorn main:app --host 0.0.0.0 --port 8081 --reload`

**Frontend**: Run from `frontend/` directory with `npm run dev`

## Important Notes

- No authentication is configured by default - add as needed
- Database automatically creates tables on startup
- Frontend proxies `/api/*` requests to backend during development
- Uses PostgreSQL for data persistence
