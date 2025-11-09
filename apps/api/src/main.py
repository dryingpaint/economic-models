"""FastAPI application for economic models platform."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.src.routes.solow import router as solow_router

app = FastAPI(
    title="Economic Models API",
    description="REST API for economic model simulations and analysis",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(solow_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Economic Models API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
