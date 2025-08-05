from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.alerts.notifier import check_negative_sentiment
from app.analytics import services
from app.core.database import get_db
from app.core.logger import logger
from app.nlp.schemas import SentimentOut, TextIn
from app.nlp.sentiment import analyze_sentiment

router = APIRouter(prefix="/listening", tags=["listening"])


@router.post("/analyze", response_model=SentimentOut)
async def analyze(req: TextIn, db: AsyncSession = Depends(get_db)):
    score = analyze_sentiment(req.text)
    await services.save_brand_mention(db, req.text, score)
    await check_negative_sentiment(db)
    logger.info("sentiment analyzed", text=req.text, sentiment=score)
    return SentimentOut(text=req.text, sentiment=score)
