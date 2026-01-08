from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from lib.api import router as api_router
from lib.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup


app = FastAPI(
    title="App API",
    description="Fullstack web application template API",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
# In development: allow localhost:3000
# In production: configure with environment variables
allowed_origins = [
    "http://localhost:3000",  # Development frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "API is running. Frontend is at http://localhost:3000",
        "docs": "/docs",
        "redoc": "/redoc"
    }


def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)


if __name__ == "__main__":
    main()
