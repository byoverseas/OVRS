from typing import Dict, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.models import BrandMention, CampaignPerformance, UserInteraction
from app.analytics.schemas import (CampaignIn, CampaignOut, CampaignMetrics,
                                   FunnelStats, InteractionIn)
from app.core.logger import logger


def compute_metrics(data: CampaignIn) -> CampaignMetrics:
    ctr = data.clicks / data.impressions if data.impressions else 0
    cpa = data.spend / data.conversions if data.conversions else 0
    roi = (data.revenue - data.spend) / data.spend if data.spend else 0
    return CampaignMetrics(ctr=ctr, cpa=cpa, roi=roi)


def get_optimization_tips(metrics: CampaignMetrics) -> List[str]:
    tips: List[str] = []
    if metrics.ctr < 0.02:
        tips.append("Low CTR, test new creatives")
    if metrics.cpa > 50:
        tips.append("High CPA, try narrowing audience")
    if metrics.roi < 0.2:
        tips.append("Low ROI, re-evaluate spend")
    return tips


async def record_campaign_data(db: AsyncSession, data: List[CampaignIn]) -> List[CampaignOut]:
    results: List[CampaignOut] = []
    for item in data:
        db.add(CampaignPerformance(**item.model_dump()))
        metrics = compute_metrics(item)
        tips = get_optimization_tips(metrics)
        logger.info("campaign ingested", platform=item.platform, metrics=metrics.model_dump(), tips=tips)
        results.append(CampaignOut(platform=item.platform, tips=tips, **metrics.model_dump()))
    await db.commit()
    return results


async def record_interaction(db: AsyncSession, interaction: InteractionIn) -> None:
    db.add(UserInteraction(**interaction.model_dump()))
    await db.commit()
    logger.info("interaction recorded", **interaction.model_dump())


async def get_attribution_summary(db: AsyncSession) -> Dict[str, Dict[str, int]]:
    stmt = select(UserInteraction.platform, UserInteraction.stage, func.count()).group_by(
        UserInteraction.platform, UserInteraction.stage
    )
    rows = await db.execute(stmt)
    summary: Dict[str, Dict[str, int]] = {}
    for platform, stage, count in rows.all():
        summary.setdefault(platform, {})[stage] = count
    return summary


async def get_funnel_stats(db: AsyncSession) -> FunnelStats:
    stages = ["impression", "click", "signup", "purchase"]
    counts: Dict[str, int] = {}
    for stage in stages:
        result = await db.execute(select(func.count()).where(UserInteraction.stage == stage))
        counts[stage] = result.scalar_one()
    return FunnelStats(
        impressions=counts.get("impression", 0),
        clicks=counts.get("click", 0),
        signups=counts.get("signup", 0),
        purchases=counts.get("purchase", 0),
    )


async def save_brand_mention(db: AsyncSession, text: str, sentiment: float) -> None:
    db.add(BrandMention(text=text, sentiment=sentiment))
    await db.commit()
    logger.info("mention stored", text=text, sentiment=sentiment)
