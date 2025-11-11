from maxo import Router

from .deeplink import deeplinks_router

commands_router = Router(__name__)

commands_router.include(
    deeplinks_router,
)
