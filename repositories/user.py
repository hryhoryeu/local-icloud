from uuid import UUID

from sqlalchemy import orm as so
import sqlalchemy as sa
import structlog

from repositories.base_repository import BaseRepository
from models.user import DBUser
from models.user_group import DBUserGroup
from errors import InternalError

logger = structlog.getLogger(__name__)


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, *, db: so.Session) -> None:
        super().__init__(db=db, entity_type=DBUser)

    def assign_group(self, *, user_id: UUID = None, group_id: UUID = None) -> None:
        db_user = self.db.get(DBUser, user_id)
        db_user_group = self.db.get(DBUserGroup, group_id)

        if db_user and db_user_group:
            db_user.groups.append(db_user_group)
            self.db.flush()
            return

        logger.info("No `db_user` or `db_user_group`")
        raise InternalError("Oops... Something went wrong")

    def get_by_email(self, *, email: str) -> DBUser:
        return self.db.scalar(sa.select(DBUser).where(DBUser.email == email))
