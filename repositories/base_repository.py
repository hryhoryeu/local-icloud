from typing import TypeVar, Generic
from abc import ABC

from sqlalchemy import orm as so
import sqlalchemy as sa

from models import Base
from errors import AlreadyExistsError

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):
    def __init__(self, *, entity_type: type[T], db: so.Session) -> None:
        self.db = db
        self.entity_type = entity_type

    def create_or_update(self, *, entity: T, commit: bool = False) -> T:
        entity = self.db.merge(entity)
        try:
            if commit:
                self.db.commit()
            else:
                self.db.flush()
        except sa.exc.IntegrityError as e:
            self.db.rollback()

            raise AlreadyExistsError(f"Integrity error: {str(e.orig)}") from e
        return entity

    def get_all(self) -> list[T]:
        query = sa.select(self.entity_type)
        return list(self.db.scalars(query))
