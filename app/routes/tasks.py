from fastapi import APIRouter, BackgroundTasks

from app.tasks.background import log_message

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/log")
async def log_task(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(log_message, message)
    return {"status": "scheduled"}
