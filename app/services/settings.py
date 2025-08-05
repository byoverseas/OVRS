from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system_settings import SystemSettings


async def update_settings(db: AsyncSession, updates: dict[str, Any]) -> None:
    for field, value in updates.items():
        key = field.upper()
        existing = await db.get(SystemSettings, key)
        if existing:
            existing.value = str(value)
        else:
            db.add(SystemSettings(key=key, value=str(value)))
    await db.commit()
