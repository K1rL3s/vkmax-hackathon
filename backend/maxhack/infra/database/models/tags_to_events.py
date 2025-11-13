from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from maxhack.core.ids import EventId, TagId
from maxhack.infra.database.models.base import BaseAlchemyModel


# TODO: Сделать IdMixin и убрать pk с tag_id, event_id,
# сделать индекс на уникальную пару tag_id + event_id
class TagsToEvents(BaseAlchemyModel):
    __tablename__ = "tags_to_events"

    tag_id: Mapped[TagId] = mapped_column(
        ForeignKey("tags.id"),
        nullable=False,
        primary_key=True,
    )
    event_id: Mapped[EventId] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
        primary_key=True,
    )
