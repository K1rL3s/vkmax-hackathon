from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from maxhack.core.ids import GroupId, InviteId, InviteKey, UserId
from maxhack.database.models._mixins import IdMixin
from maxhack.database.models.base import BaseAlchemyModel

INVITE_KEY_LEN = 8


class InviteModel(BaseAlchemyModel, IdMixin[InviteId]):
    __tablename__ = "invites"

    key: Mapped[InviteKey] = mapped_column(
        String(INVITE_KEY_LEN),
        nullable=False,
        unique=True,
    )
    creator_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"), nullable=False)
    group_id: Mapped[GroupId] = mapped_column(ForeignKey("groups.id"), nullable=False)
