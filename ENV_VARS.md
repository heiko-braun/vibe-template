# Environment Variables Reference

This document lists all environment variables used in the application.

## Backend Environment Variables

Located in `backend/.env` (copy from `backend/.env.example`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/app` | PostgreSQL connection string |
| `FRONTEND_URL` | No | `http://localhost:3000` | Frontend URL for CORS configuration |

### Backend Examples

**Local Development:**
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
FRONTEND_URL=http://localhost:3000
```

**Production:**
```bash
DATABASE_URL=postgresql://user:pass@db.example.com:5432/production_db
FRONTEND_URL=https://yourdomain.com
```

## Frontend Environment Variables

Located in `frontend/.env` (copy from `frontend/.env.example`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NUXT_PUBLIC_API_BASE_URL` | No | `http://localhost:8081` | Backend API base URL |

### Frontend Examples

**Local Development:**
```bash
NUXT_PUBLIC_API_BASE_URL=http://localhost:8081
```

**Production:**
```bash
NUXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
```

**Important Note:** In production, this variable MUST be set as an environment variable during the build process (not just at runtime). It gets baked into the JavaScript bundle during `npm run build`.

## How Environment Variables Work

### Backend (FastAPI)
- Uses `python-dotenv` to load `.env` file
- Environment variables are read via `os.getenv()` or `pydantic-settings`
- Variables can be overridden by system environment variables

### Frontend (Nuxt)
- Uses Nuxt's built-in environment variable handling
- Variables prefixed with `NUXT_PUBLIC_` are exposed to the browser
- Variables are read at build time and baked into the bundle
- Can be overridden at build time via system environment variables

## Production Deployment Notes

### Setting Environment Variables

Most hosting platforms provide a way to set environment variables:
- **Platform dashboards**: Web UI for managing environment variables
- **CLI tools**: Command-line tools for configuration
- **Configuration files**: `.env` files, Docker Compose, Kubernetes ConfigMaps, etc.
- **CI/CD pipelines**: Set during build/deployment process

### Important Considerations

1. **Frontend variables must be set during build** - They're baked into the bundle at build time
2. **After changing frontend variables, rebuild** (don't just restart) - Variables are compiled into the JavaScript bundle
3. **Use HTTPS URLs in production** - Avoid mixed content errors
4. **Remove trailing slashes from URLs** - CORS matching is exact
5. **Backend variables can be changed at runtime** - Restart service after changes

## Environment Variable Checklist

### Local Development Setup
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Set `DATABASE_URL` to your local PostgreSQL
- [ ] Copy `frontend/.env.example` to `frontend/.env` (optional, defaults work)

### Production Deployment
- [ ] Set `DATABASE_URL` in backend service environment
- [ ] Set `FRONTEND_URL` in backend service environment (your frontend domain)
- [ ] Set `NUXT_PUBLIC_API_BASE_URL` during frontend build process (your backend API domain)
- [ ] Verify all URLs use HTTPS (not HTTP)
- [ ] Verify no trailing slashes in URLs
- [ ] Configure SSL/TLS certificates for both services

## Troubleshooting

### Backend can't connect to database
- Check `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Verify PostgreSQL is running
- Check credentials are correct

### Frontend can't connect to backend
- Check `NUXT_PUBLIC_API_BASE_URL` is set correctly
- In production, verify it's set during the build process
- Check backend is accessible at the URL
- Verify HTTPS is used in production
- Check browser console for specific error messages

### CORS errors
- Check `FRONTEND_URL` in backend matches your actual frontend URL
- Verify no trailing slashes
- In production, both services should use HTTPS
