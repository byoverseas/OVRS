from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.models.user import User
from app.services.role import get_role_by_name
from app.services.user import get_user_by_username


async def invite_user_to_team(
    session: AsyncSession, username: str, team_id: int, role_name: str
) -> User:
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = await get_role_by_name(session, role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    team = await session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    user.team_id = team_id
    user.role_id = role.id
    user.company_id = team.company_id
    await session.commit()
    await session.refresh(user)
    return user


async def assign_role(
    session: AsyncSession, username: str, team_id: int, role_name: str
) -> User:
    return await invite_user_to_team(session, username, team_id, role_name)


async def switch_company(session: AsyncSession, user: User, company_id: int) -> User:
    user.company_id = company_id
    await session.commit()
    await session.refresh(user)
    return user
