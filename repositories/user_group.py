from sqlalchemy import orm as so

from repositories.base_repository import BaseRepository
from models.user_group import DBUserGroup


class UserGroupRepository(BaseRepository[DBUserGroup]):
    def __init__(self, *, db: so.Session) -> None:
        super().__init__(db=db, entity_type=DBUserGroup)
