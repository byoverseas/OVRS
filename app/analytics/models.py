from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class CampaignPerformance(Base):
    __tablename__ = "campaign_performance"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    spend = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    conversions = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserInteraction(Base):
    __tablename__ = "user_interaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BrandMention(Base):
    __tablename__ = "brand_mention"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
