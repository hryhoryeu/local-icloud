from sqlalchemy import orm as so
from argon2 import PasswordHasher

from schemas.user import User, UserResponse, UserInDB
from models.user import DBUser
from repositories.user import UserRepository
from services.base_service import BaseService


class UserService(BaseService[User, UserResponse, UserRepository]):
    def __init__(self, *, db: so.Session) -> None:
        super().__init__(db=db)
        self.repo = UserRepository(db=db)

    def add(self, *, entity: User) -> UserRepository:
        user_dict = self.map_user_to_dict(user=entity)
        user_dict["hashed_password"] = self.__hash_password(
            password=user_dict.pop("password")
        )

        db_user = DBUser(**user_dict)

        db_user = self.repo.create_or_update(entity=db_user)

        self.db.commit()

        return UserResponse.model_validate(db_user)

    def get_all(self) -> list[UserRepository]:
        db_users = self.repo.get_all()

        return [UserResponse.model_validate(u) for u in db_users]

    def map_user_to_dict(self, *, user: User) -> dict:
        return user.model_dump()

    def __hash_password(self, *, password: str) -> str:
        ph = PasswordHasher()
        return ph.hash(password)

    def get_by_email(self, *, email: str) -> UserInDB:
        db_user = self.repo.get_by_email(email=email)

        return UserInDB.model_validate(db_user)
