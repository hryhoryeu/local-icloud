from helpers import hash_password
from settings import secrets
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped, load_only
from errors import AlreadyExistsError
import uuid
from models import UserResponse

engine = create_engine(
    f"postgresql+psycopg://{secrets.PG_USER}:{secrets.PG_PASSWORD}@{secrets.PG_HOST}:{secrets.PG_PORT}/{secrets.PG_DB}"
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    disabled: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User(id={self.id!r}, email={self.email!r}), is_superuser={self.is_superuser!r}), disabled={self.disabled!r})>"


def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
    disabled: bool = False,
) -> User:
    with Session(engine) as session:
        if session.execute(select(User).filter(User.email == email)).scalar():
            raise AlreadyExistsError(detail=f"User '{email}' already exists")

        hashed_password = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_superuser=is_superuser,
            disabled=disabled,
        )
        session.add(user)
        session.commit()
        return UserResponse.model_validate(user)


def get_all_users() -> list[User]:
    with Session(engine) as session:
        users = session.scalars(
            select(User).options(load_only(User.id, User.email, User.is_superuser))
        ).all()
        return [UserResponse.model_validate(user) for user in users]


def create_db():
    Base.metadata.create_all(engine)
