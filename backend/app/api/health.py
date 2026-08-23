from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.core.config import settings
from app.core.brightdata_config import brightdata_settings
from app.core.database import check_database_connection

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Upgraded Observability Health Check"
)
async def health_check():
    db_ok = check_database_connection()
    bd_configured = bool(brightdata_settings.BRIGHT_DATA_COLLECTOR_ID and brightdata_settings.api_key)
    status_str = "healthy" if db_ok else "degraded"

    return {
        "status": status_str,
        "database": "connected" if db_ok else "disconnected",
        "bright_data": "configured" if bd_configured else "unconfigured",
        "version": settings.VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
