from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import require_role
from app.core.config import reload_settings, settings
from app.core.database import get_db
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.services.settings import update_settings

router = APIRouter(prefix="/op", tags=["op"], dependencies=[Depends(require_role(["admin"]))])


def _serialize_settings() -> dict:
    return {
        "jwt_expiration_hours": settings.jwt_expiration_hours,
        "bcrypt_salt_rounds": settings.bcrypt_salt_rounds,
        "enable_logging": settings.enable_logging,
        "enable_background_tasks": settings.enable_background_tasks,
        "default_export_format": settings.default_export_format,
        "negative_sentiment_threshold": settings.negative_sentiment_threshold,
    }


@router.get("/settings", response_model=SettingsResponse)
async def read_settings(db: AsyncSession = Depends(get_db)):
    await reload_settings(db)
    return SettingsResponse(**_serialize_settings())


@router.post("/settings", response_model=SettingsResponse)
async def write_settings(update: SettingsUpdate, db: AsyncSession = Depends(get_db)):
    await update_settings(db, update.model_dump(exclude_unset=True))
    await reload_settings(db)
    return SettingsResponse(**_serialize_settings())
