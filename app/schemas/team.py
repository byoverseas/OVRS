from pydantic import BaseModel


class TeamInvite(BaseModel):
    username: str
    team_id: int
    role: str


class RoleAssign(BaseModel):
    username: str
    team_id: int
    role: str


class SwitchCompany(BaseModel):
    company_id: int
