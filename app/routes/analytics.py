from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics import services
from app.analytics.schemas import (CampaignIn, CampaignOut, FunnelStats,
                                   InteractionIn)
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/ingest", response_model=list[CampaignOut])
async def ingest_campaign(data: list[CampaignIn], db: AsyncSession = Depends(get_db)):
    return await services.record_campaign_data(db, data)


@router.post("/interaction")
async def add_interaction(interaction: InteractionIn, db: AsyncSession = Depends(get_db)):
    await services.record_interaction(db, interaction)
    return {"status": "ok"}


@router.get("/attribution")
async def attribution(db: AsyncSession = Depends(get_db)):
    return await services.get_attribution_summary(db)


@router.get("/funnel", response_model=FunnelStats)
async def funnel(db: AsyncSession = Depends(get_db)):
    return await services.get_funnel_stats(db)
