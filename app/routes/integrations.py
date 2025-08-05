from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.schemas import CampaignIn
from app.analytics.services import record_campaign_data
from app.alerts.notifier import publish_alert
from app.auth.deps import require_role
from app.core.config import settings
from app.core.database import get_db
from app.routes.export import export_campaigns

router = APIRouter(prefix="/integrations/n8n", tags=["n8n"])


def verify_webhook(token: str = Header(..., alias="X-Webhook-Token")):
    if settings.n8n_webhook_token and token != settings.n8n_webhook_token:
        raise HTTPException(status_code=403, detail="Invalid webhook token")


@router.post(
    "/alerts", dependencies=[Depends(verify_webhook), Depends(require_role(["admin"]))]
)
async def trigger_alert(payload: dict):
    await publish_alert(payload.get("message", "n8n alert"))
    return {"status": "alert sent"}


@router.post(
    "/ingest", dependencies=[Depends(verify_webhook), Depends(require_role(["admin"]))]
)
async def ingest(data: list[CampaignIn], db: AsyncSession = Depends(get_db)):
    await record_campaign_data(db, data)
    return {"status": "ingested"}


@router.get(
    "/export", dependencies=[Depends(verify_webhook), Depends(require_role(["admin"]))]
)
async def n8n_export(
    format: str = "json",
    platform: str | None = None,
    stage: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await export_campaigns(
        format=format,
        platform=platform,
        stage=stage,
        start_date=start_date,
        end_date=end_date,
        db=db,
    )
