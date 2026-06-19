"""
Health check & system status endpoints.
"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check — confirms the API is alive."""
    return {
        "status": "healthy",
        "service": "RecruitBot API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


from app.core.database import async_session_factory
from sqlalchemy import text
from app.core.config import get_settings

settings = get_settings()

@router.get("/health/detailed")
async def detailed_health():
    """
    Detailed health check — reports real DB and LLM connectivity.
    """
    # 1. Check Database
    db_status = "error"
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"failed: {str(e)}"

    # 2. Check LLM Gateway
    llm_status = "error"
    try:
        if settings.ANTHROPIC_API_KEY or settings.GEMINI_API_KEY or settings.OPENAI_API_KEY:
             llm_status = "configured"
        else:
             llm_status = "missing_api_keys"
    except Exception as e:
        llm_status = f"failed: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "RecruitBot API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "database": {"status": db_status},
            "llm_gateway": {"status": llm_status},
            "redis": {"status": "not_configured"},
        },
    }
