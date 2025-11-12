from dataclasses import dataclass
from typing import Any, Self


@dataclass(slots=True, kw_only=True)
class DomainModel:
    """Базовая модель доменной сущности"""

    def to_dict(
        self: Self,
        exclude: set[str] | None = None,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        """Преобразует модель в словарь.

        Args:
            exclude (set[str] | None): Множество полей для исключения из словаря
            exclude_none (bool, optional): Исключать ли пустые поля
            Defaults to False.

        Returns:
            dict[str, Any]: Словарь представления модели
        """
        exclude = exclude or set()
        return {
            k: v
            for k, v in self.__dict__.items()
            if k not in exclude and (not exclude_none or v is not None)
        }
