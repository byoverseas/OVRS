import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.models import CampaignPerformance, UserInteraction
from app.auth.deps import require_role
from app.core.database import get_db

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/", dependencies=[Depends(require_role(["admin"]))])
async def export_campaigns(
    format: str = "json",
    platform: str | None = None,
    stage: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CampaignPerformance)
    if platform:
        stmt = stmt.where(CampaignPerformance.platform == platform)
    if start_date:
        stmt = stmt.where(CampaignPerformance.created_at >= start_date)
    if end_date:
        stmt = stmt.where(CampaignPerformance.created_at <= end_date)
    if stage:
        stmt = stmt.join(
            UserInteraction,
            UserInteraction.platform == CampaignPerformance.platform,
        ).where(UserInteraction.stage == stage)
    result = await db.execute(stmt)
    records = result.scalars().all()
    data = [
        {
            "platform": r.platform,
            "impressions": r.impressions,
            "clicks": r.clicks,
            "spend": r.spend,
            "revenue": r.revenue,
            "conversions": r.conversions,
        }
        for r in records
    ]
    if format == "csv":
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "platform",
                "impressions",
                "clicks",
                "spend",
                "revenue",
                "conversions",
            ],
        )
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return Response(content=buffer.getvalue(), media_type="text/csv")
    return data
