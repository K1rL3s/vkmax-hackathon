from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from maxhack.core.ids import GroupId
from maxhack.database.models._mixins import IdMixin
from maxhack.database.models.base import BaseAlchemyModel

GROUP_NAME_LEN = 128
GROUP_DESCRIPTION_LEN = 1024


class GroupModel(BaseAlchemyModel, IdMixin[GroupId]):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(GROUP_NAME_LEN), nullable=False)
    description: Mapped[str] = mapped_column(
        String(GROUP_DESCRIPTION_LEN),
        nullable=True,
    )
    timezone: Mapped[int] = mapped_column(Integer, nullable=False)
