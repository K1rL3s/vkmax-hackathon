from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

healthcheck_router = APIRouter(
    prefix="/health",
    tags=["Healthcheck"],
    route_class=DishkaRoute,
)


@healthcheck_router.get(
    "",
    description="Проверка соединения",
)
async def check_connection() -> None:
    return
