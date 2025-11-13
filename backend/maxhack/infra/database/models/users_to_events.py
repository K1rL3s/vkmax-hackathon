from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from maxhack.core.ids import EventId, UserId
from maxhack.infra.database.models.base import BaseAlchemyModel


# TODO: Добавить IdMixin и убрать pk с user_id event_id,
# добавить индекс на уникальную пару
class UsersToEvents(BaseAlchemyModel):
    __tablename__ = "users_to_events"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
    )
    event_id: Mapped[EventId] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
        primary_key=True,
    )
