from pathlib import Path
import sys
from loguru import logger

from app.core.config import settings

# Ensure log directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()
# Log to stdout in JSON
logger.add(sys.stdout, level=settings.log_level, serialize=True)
# Log to rotating file
logger.add(LOG_DIR / "app.log", rotation=settings.log_rotation, serialize=True)
