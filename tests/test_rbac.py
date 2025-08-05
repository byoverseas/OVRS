import pytest
from fastapi import HTTPException

from app.auth.deps import require_role


class DummyUser:
    def __init__(self, role_name: str | None):
        class RoleObj:
            def __init__(self, name: str | None):
                self.name = name

        self.role = RoleObj(role_name)


@pytest.mark.asyncio
async def test_require_role_allows_admin():
    checker = require_role(["admin"])
    user = DummyUser("admin")
    assert await checker(current_user=user) == user


@pytest.mark.asyncio
async def test_require_role_blocks_viewer():
    checker = require_role(["admin"])
    user = DummyUser("viewer")
    with pytest.raises(HTTPException):
        await checker(current_user=user)
