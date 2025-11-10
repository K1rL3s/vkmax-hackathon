from .core import Model


class UserCreateRequest(Model):
    max_id: int
    max_chat_id: int
    first_name: str
    last_name: str | None = None
    phone: str | None = None
    timezone: int = 0


class UserUpdateRequest(Model):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserResponse(Model):
    id: int
    max_id: int
    first_name: str
    last_name: str | None = None
    phone: str
    timezone: int


class UserGroupItem(Model):
    group_id: int
    name: str
    description: str | None = None
    role_id: int


class UserGroupsResponse(Model):
    groups: list[UserGroupItem]
