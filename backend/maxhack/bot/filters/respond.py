from dataclasses import dataclass

from maxo.routing.filters.payload import Payload

from maxhack.core.enums.respond_action import RespondStatus


@dataclass
class RespondData(Payload, prefix="respond"):
    event_id: int
    status: RespondStatus
