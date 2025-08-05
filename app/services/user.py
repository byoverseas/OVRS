from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.role import get_role_by_name


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    role = None
    if user.role:
        role = await get_role_by_name(session, user.role)
    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role_id=role.id if role else None,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    db_user = await get_user_by_username(session, username)
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user
