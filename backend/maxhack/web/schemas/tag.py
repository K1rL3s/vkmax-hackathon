from .core import Model
from maxhack.core.ids import GroupId, RoleId, TagId, UserId


class TagCreateRequest(Model):
    name: str
    description: str | None = None
    color: str


class TagUpdateRequest(Model):
    name: str | None = None
    description: str | None = None
    color: str | None = None


class TagResponse(Model):
    id: UserId
    group_id: GroupId
    name: str
    description: str | None = None
    color: str


class TagAssignRequest(Model):
    user_id: UserId
    tag_id: TagId


class TagUserItem(Model):
    user_id: UserId
    max_id: int
    first_name: str
    last_name: str | None = None
    phone: str | None = None
    role_id: RoleId
