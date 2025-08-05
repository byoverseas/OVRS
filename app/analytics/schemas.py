from typing import Dict, List

from pydantic import BaseModel, Field


class CampaignIn(BaseModel):
    platform: str
    impressions: int
    clicks: int
    spend: float
    revenue: float
    conversions: int


class CampaignMetrics(BaseModel):
    ctr: float = Field(..., description="Click-through rate")
    cpa: float = Field(..., description="Cost per acquisition")
    roi: float = Field(..., description="Return on investment")


class CampaignOut(CampaignMetrics):
    platform: str
    tips: List[str]


class InteractionIn(BaseModel):
    user_id: str
    platform: str
    stage: str


class FunnelStats(BaseModel):
    impressions: int
    clicks: int
    signups: int
    purchases: int
