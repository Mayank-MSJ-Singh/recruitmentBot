"""
RecruitBot — FastAPI Application Entry Point

An End-to-End Agentic Recruitment Orchestrator.
From job requisition to first day of onboarding.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.core.config import get_settings
from app.api.routes import api_router

# Load environment variables from root .env
load_dotenv(dotenv_path="../../.env")

settings = get_settings()

from app.core.database import engine
from app.services.llm import llm_gateway

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    Startup: initialize DB connections, LLM clients, workers, etc.
    Shutdown: close connections gracefully.
    """
    # ── Startup ──
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    # (Sprint 0.2): Initialize database connection pool
    # Engine is initialized in core.database, ping to check
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection established.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    # (Sprint 0.3): Initialize LLM Gateway client
    # Trigger initialization or logging if needed
    print(f"✅ LLM Gateway initialized with default premium model: {llm_gateway.model_premium}")

    # TODO (Sprint 0.4): Initialize auth provider
    yield
    # ── Shutdown ──
    print(f"👋 {settings.APP_NAME} shutting down...")
    await engine.dispose()
    print("✅ Database connection pool closed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "An autonomous AI recruiter that orchestrates the entire hiring lifecycle — "
        "from job requisition to first day of onboarding."
    ),
    lifespan=lifespan,
)

# ── CORS — allow the Vite dev server in development ──
# In production, the Vite proxy handles this; CORS is a safety net.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register all API routes under /api/v1 ──
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ── Root redirect ──
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint — basic info for anyone hitting the bare URL."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
    }
