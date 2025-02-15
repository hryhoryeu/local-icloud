from sqlalchemy import orm as so

from schemas.user_group import UserGroup, UserGroupResponse
from models.user_group import DBUserGroup
from repositories.user_group import UserGroupRepository
from services.base_service import BaseService


class UserGroupService(BaseService[UserGroup, UserGroupResponse, UserGroupRepository]):
    def __init__(self, *, db: so.Session) -> None:
        super().__init__(db=db)
        self.repo = UserGroupRepository(db=db)

    def add(self, *, entity: UserGroup) -> UserGroupResponse:
        db_user_group = DBUserGroup(**entity.model_dump())
        db_user_group = self.repo.create_or_update(entity=db_user_group)

        self.db.flush()
        self.db.commit()

        return UserGroupResponse.model_validate(db_user_group)

    def get_all(self) -> list[UserGroupResponse]:
        db_user_groups = self.repo.get_all()

        return [UserGroupResponse.model_validate(ug) for ug in db_user_groups]
