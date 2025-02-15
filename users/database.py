from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from helpers import hash_password
from models.user import DBUser
from schemas.user import UserResponse
from errors import AlreadyExistsError
from database import engine


def create_user(
    email: str,
    password: str,
    disabled: bool = False,
) -> UserResponse:
    with Session(engine) as session:
        if session.execute(select(DBUser).filter(DBUser.email == email)).scalar():
            raise AlreadyExistsError(detail=f"User '{email}' already exists")

        hashed_password = hash_password(password)
        user = DBUser(
            email=email,
            hashed_password=hashed_password,
            disabled=disabled,
        )
        session.add(user)
        session.commit()
        return UserResponse.model_validate(user)


def get_all_users() -> list[UserResponse]:
    with Session(engine) as session:
        users = session.scalars(
            select(DBUser).options(
                load_only(DBUser.id, DBUser.email, DBUser.is_superuser)
            )
        ).all()
        return [UserResponse.model_validate(user) for user in users]
