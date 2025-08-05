from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / '.env'


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    secret_key: str
    jwt_expiration_hours: int = 24
    bcrypt_salt_rounds: int = 12
    allowed_origins: str | None = None
    database_url: str = 'sqlite+aiosqlite:///./test.db'
    env: str = 'development'
    db_pool_size: int = 5
    db_max_overflow: int = 10
    log_level: str = 'INFO'
    log_rotation: str = '10 MB'
    redis_url: str = 'redis://redis:6379/0'
    celery_broker_url: str = 'redis://redis:6379/0'
    celery_result_backend: str = 'redis://redis:6379/0'
    n8n_webhook_token: str | None = None

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), case_sensitive=False)


settings = Settings()
