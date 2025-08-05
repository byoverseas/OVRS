import pytest
from datetime import datetime
from jose import jwt

from sqlalchemy import delete

from app.auth.security import create_access_token
from app.core.config import reload_settings, settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models.system_settings import SystemSettings

ALGORITHM = "HS256"


@pytest.mark.asyncio
async def test_jwt_expiration_override():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await session.execute(delete(SystemSettings))
        session.add(SystemSettings(key="JWT_EXPIRATION_HOURS", value="1"))
        await session.commit()
        await reload_settings(session)
        token = create_access_token("tester")
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"])
        delta = exp - datetime.utcnow()
        assert 3500 <= delta.total_seconds() <= 3700
