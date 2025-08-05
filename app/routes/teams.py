from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user, require_role
from app.core.database import get_db
from app.schemas.team import RoleAssign, SwitchCompany, TeamInvite
from app.services.team import assign_role, invite_user_to_team, switch_company

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/invite", dependencies=[Depends(require_role(["admin"]))])
async def invite(invite: TeamInvite, db: AsyncSession = Depends(get_db)):
    user = await invite_user_to_team(db, invite.username, invite.team_id, invite.role)
    return {"message": f"User {user.username} invited"}


@router.post("/assign", dependencies=[Depends(require_role(["admin"]))])
async def assign(role: RoleAssign, db: AsyncSession = Depends(get_db)):
    user = await assign_role(db, role.username, role.team_id, role.role)
    return {"message": f"Role updated for {user.username}"}


@router.post("/switch-company")
async def switch_company_route(
    payload: SwitchCompany,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await switch_company(db, current_user, payload.company_id)
    return {"active_company": user.company_id}
