from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-ready FastAPI backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router, prefix='/api/v1')