from uuid import UUID

from sqlalchemy import orm as so
import sqlalchemy as sa

from repositories.base_repository import BaseRepository
from models.user import DBUser
from models.user_group import DBUserGroup


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, *, db: so.Session) -> None:
        super().__init__(db=db, entity_type=DBUser)

    def assign_group(self, user_id: UUID = None, group_id: UUID = None) -> DBUser:
        import ipdb

        ipdb.set_trace()
        db_user = self.db.get(DBUser, user_id)
        db_user_group = self.db.get(DBUserGroup, group_id)

        if db_user and db_user_group:
            db_user.groups

        # db_user.groups.

    def list_user_groups(self, user) -> list[DBUserGroup]:
        sa.select(DBUserGroup)

    def get_by_email(self, *, email: str) -> DBUser:

        return self.db.scalar(sa.select(DBUser).where(DBUser.email == email))
