from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings, settings
from app.models.user import User

from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from fastapi_healthcheck_sqlalchemy import HealthCheckSQLAlchemy
from fastapi_healthcheck_uri import HealthCheckUri

router = APIRouter()



# Add Health Checks
_healthChecks = HealthCheckFactory()
_healthChecks.add(HealthCheckUri(alias='google.com', connectionUri="https://google.com", tags=('external', 'google', 'aww')))


@router.get("/health")
async def health_full(settings: Settings = Depends(get_settings)):
    return _healthChecks.check()

@router.get("/health/live")
async def health_live(settings: Settings = Depends(get_settings)):
    return {"status": "OK"}

@router.get("/health/ready")
async def health_ready(settings: Settings = Depends(get_settings)):
    if True:
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=503, detail="Not ready")

@router.get("/health/started")
async def health_started(settings: Settings = Depends(get_settings)):
    return {"status": "OK"}
