from inspect import Parameter
from typing import Any

from dishka import Container
from dishka.integrations.base import wrap_injection

CONTAINER_NAME = "request_dishka_container"


def pytest_inject(func: Any) -> Any:
    additional_params = [
        Parameter(
            name=CONTAINER_NAME,
            annotation=Container,
            kind=Parameter.KEYWORD_ONLY,
        ),
    ]
    return wrap_injection(
        func=func,
        remove_depends=True,
        container_getter=lambda _, p: p[CONTAINER_NAME],
        additional_params=additional_params,
        is_async=True,
    )
