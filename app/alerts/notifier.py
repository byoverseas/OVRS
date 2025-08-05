import json
from datetime import datetime, timedelta

from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.models import BrandMention
from app.core.config import settings

redis = Redis.from_url(settings.redis_url)


async def publish_alert(message: str) -> None:
    await redis.publish("alerts", json.dumps({"message": message}))


async def check_negative_sentiment(db: AsyncSession) -> None:
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    stmt = select(func.count(BrandMention.id)).where(
        BrandMention.sentiment < -0.5, BrandMention.created_at >= one_hour_ago
    )
    result = await db.execute(stmt)
    count = result.scalar_one()
    if count >= settings.negative_sentiment_threshold:
        await publish_alert("High negative sentiment detected")
