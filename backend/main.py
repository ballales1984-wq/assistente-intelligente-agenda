"""
Assistente Intelligente - FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import engine, sync_engine, Base, get_db
from app.models.schemas import *
from app.api.routes import router
from config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crea tabelle
    Base.metadata.create_all(bind=sync_engine)
    print("✅ Database pronto")
    yield
    # Shutdown
    print("👋 Shutdown")


app = FastAPI(
    title="Assistente Intelligente API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
origins = [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "app": "Assistente Intelligente API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
