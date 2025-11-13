from typing import Literal, cast

import fastapi
from dishka.integrations.fastapi import setup_dishka
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from maxhack.config import load_config
from maxhack.core.exceptions import EntityNotFound, InvalidValue, NotEnoughRights
from maxhack.di import make_container
from maxhack.logger import get_logger
from maxhack.utils.log_config import set_logging
from maxhack.web.routes import (
    auth_router,
    event_router,
    group_router,
    healthcheck_router,
    tag_router,
    user_router,
)

logger = get_logger(__name__)

tags_metadata = [
    {
        "name": "Healthcheck",
        "description": "Роут для проверки соединения приложения с базой данных",
    },
    {
        "name": "Auth",
        "description": "Роут для проверки WebAppData при запуске мини-аппа",
    },
]

description = """
### Права доступа к сущностям

Для каждой сущности предусмотрен определённый набор прав, которые, в зависимости от логики, могут назначаться различному
набору ролей. Также, помимо основного набора прав, ограничения могут быть выставлены непосредственно на уровне определённых ролей.
"""
app = fastapi.FastAPI(
    title="Таск трекер для МАКС",
    description=description,
    version="0.1.0",
    openapi_tags=sorted(tags_metadata, key=lambda i: i["name"]),
    swagger_ui_parameters={
        "docExpansion": "none",
        "displayRequestDuration": "true",
        "syntaxHighlight.theme": "obsidian",
        "tryItOutEnabled": "true",
        "requestSnippetsEnabled": "true",
    },
)

config = load_config()
container = make_container(config=config)
setup_dishka(container, app)

app.include_router(healthcheck_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(tag_router)
app.include_router(event_router)

set_logging(
    level=cast(Literal["DEBUG", "INFO", "ERROR", "WARNING"], config.log_level),
    enable_additional_debug=config.app.additional_debug,
    app=app,
)

default_errors = {
    401: {"description": "Unauthorized"},
    403: {"description": "No permission"},
    404: {"description": "Object not found"},
    409: {"description": "Collision occurred. Entity already exists"},
    410: {"description": "Already Expired"},
}


async def value_error_exception_handler(
    request: Request,
    exc: ValueError,
) -> JSONResponse:
    logger.warning("409_CONFLICT", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def entity_not_found_exception_handler(
    request: Request,
    exc: EntityNotFound,
) -> JSONResponse:
    logger.warning("404_NOT_FOUND", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def not_enough_rights_exception_handler(
    request: Request,
    exc: NotEnoughRights,
) -> JSONResponse:
    logger.warning("404_NOT_FOUND", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


async def invalid_value_exception_handler(
    request: Request,
    exc: InvalidValue,
) -> JSONResponse:
    logger.warning("409_CONFLICT", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def unknown_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("500_INTERNAL_SERVER_ERROR", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


app.add_exception_handler(ValueError, value_error_exception_handler)
app.add_exception_handler(EntityNotFound, entity_not_found_exception_handler)
app.add_exception_handler(NotEnoughRights, not_enough_rights_exception_handler)
app.add_exception_handler(InvalidValue, invalid_value_exception_handler)
app.add_exception_handler(Exception, unknown_exception_handler)


if config.app.cors:
    allowed_origins = ["*"] if config.app.cors_policy_disabled else config.app.cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
        allow_credentials=True,
    )

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
