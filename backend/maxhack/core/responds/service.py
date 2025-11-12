from maxhack.core.exceptions import NotEnoughRights, RespondNotFound
from maxhack.core.ids import EventId, RespondId, UserId
from maxhack.core.service import BaseService
from maxhack.infra.database.models import RespondModel


class RespondService(BaseService):
    async def create(
        self,
        user_ids: list[UserId],
        event_id: EventId,
        status: str,
    ):
        await self._respond_repo.create(user_ids, event_id, status)

    async def update(
        self,
        respond_id: RespondId,
        event_id: EventId,
        user_id: UserId,
        status: str,
    ) -> RespondModel:
        respond = await self._ensure_respond_exists(respond_id)

        if respond.user_id != user_id:
            raise NotEnoughRights("Пользователь  не может редактировать не свой отклик")
        values = {"status": status}
        respond = await self._respond_repo.update(event_id, **values)
        if respond is None:
            raise RespondNotFound

        return respond
