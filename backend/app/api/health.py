"""
Health check & system status endpoints.
"""

from fastapi import APIRouter
from datetime import datetime, timezone
from sqlalchemy import text
from app.core.database import engine
from app.services.llm import llm_gateway

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check — confirms the API is alive."""
    return {
        "status": "healthy",
        "service": "RecruitBot API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/detailed")
async def detailed_health():
    """
    Detailed health check — will report DB, Redis, LLM connectivity
    once those are wired in (Phase 0.2–0.3).
    """
    # Check Database
    db_status = "error"
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        pass

    # Check LLM Gateway
    llm_status = "configured" if llm_gateway.model_premium else "not_configured"

    components_healthy = db_status == "connected" and llm_status == "configured"

    return {
        "status": "healthy" if components_healthy else "degraded",
        "service": "RecruitBot API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "database": {"status": db_status},
            "llm_gateway": {"status": llm_status},
            "redis": {"status": "not_configured"}, # Redis is not set up in Phase 0
        },
    }
