from datetime import datetime

from maxhack.core.ids import EventId, GroupId, RespondId, TagId, UserId

from .core import Model


class EventCreateRequest(Model):
    title: str
    description: str | None = None
    event_date: datetime
    timezone: int | None = None
    every_day: bool = False
    every_week: bool = False
    every_month: bool = False
    type: str
    group_id: GroupId | None = None
    user_ids: list[UserId] | None = None
    tag_ids: list[TagId] | None = None
    minutes_before: int = 60


class EventUpdateRequest(Model):
    title: str | None = None
    description: str | None = None
    is_cycle: bool | None = None
    type: str | None = None
    timezone: int | None
    event_date: datetime | None
    every_day: bool
    every_week: bool
    every_month: bool


class EventResponse(Model):
    id: EventId
    title: str
    description: str | None = None
    cron: str
    is_cycle: bool
    type: str
    creator_id: UserId
    group_id: GroupId | None = None
    timezone: int


class EventAddTagRequest(Model):
    tag_ids: list[TagId]


class EventAddUserRequest(Model):
    user_ids: list[UserId]


class EventsResponse(Model):
    events: list[EventResponse]


class RespondChangeResponse(Model):
    status: str


class RespondResponse(Model):
    id: RespondId
    user_id: UserId
    event_id: EventId
    status: str
