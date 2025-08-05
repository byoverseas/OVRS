from pydantic import BaseModel


class SettingsResponse(BaseModel):
    jwt_expiration_hours: int
    bcrypt_salt_rounds: int
    enable_logging: bool
    enable_background_tasks: bool
    default_export_format: str
    negative_sentiment_threshold: int

    class Config:
        extra = 'ignore'


class SettingsUpdate(BaseModel):
    jwt_expiration_hours: int | None = None
    bcrypt_salt_rounds: int | None = None
    enable_logging: bool | None = None
    enable_background_tasks: bool | None = None
    default_export_format: str | None = None
    negative_sentiment_threshold: int | None = None
