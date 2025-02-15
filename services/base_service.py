from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy import orm as so
from pydantic import BaseModel

from repositories.base_repository import BaseRepository

T = TypeVar("T", bound=BaseModel)
V = TypeVar("V", bound=BaseModel)
R = TypeVar("R", bound=BaseRepository)


class BaseService(Generic[T, V, R], ABC):
    def __init__(self, *, db: so.Session) -> None:
        self.db = db
        self.repo: R

    @abstractmethod
    def add(self, *, entity: T) -> V: ...

    @abstractmethod
    def get_all(self) -> list[V]: ...
