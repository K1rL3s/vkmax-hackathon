from typing import Literal

from pydantic import Field

from maxhack.core.ids import RoleId
from maxhack.web.schemas.core import Model


class RoleResponse(Model):
    id: RoleId
    name: Literal["Босс", "Начальник", "Участник"] = Field(
        ...,
        examples=["Босс"],
    )
