from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6)
    role: str | None = "viewer"


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str | None = None

    class Config:
        orm_mode = True
