from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from maxhack.core.ids import GroupId, InviteId, InviteKey, UserId
from maxhack.infra.database.models._mixins import IdMixin
from maxhack.infra.database.models.base import BaseAlchemyModel


class InviteModel(BaseAlchemyModel, IdMixin[InviteId]):
    __tablename__ = "invites"

    key: Mapped[InviteKey] = mapped_column(String(8), nullable=False, unique=True)
    creator_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"), nullable=False)
    group_id: Mapped[GroupId] = mapped_column(ForeignKey("groups.id"), nullable=False)
