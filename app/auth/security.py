from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core import config

ALGORITHM = "HS256"


def get_pwd_context() -> CryptContext:
    return CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__rounds=config.settings.bcrypt_salt_rounds,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_pwd_context().verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return get_pwd_context().hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=config.settings.jwt_expiration_hours)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
