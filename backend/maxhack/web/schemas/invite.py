from maxhack.core.ids import InviteKey
from maxhack.web.schemas.core import Model


class InviteCreateResponse(Model):
    invite_key: InviteKey


class InviteAcceptRequest(Model):
    invite_key: InviteKey
