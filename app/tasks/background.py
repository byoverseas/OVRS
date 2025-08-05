import asyncio

from app.core.logger import logger


async def log_message(message: str) -> None:
    """Example background task that logs a message after a short delay."""
    await asyncio.sleep(1)
    logger.info("background task: {}", message)
