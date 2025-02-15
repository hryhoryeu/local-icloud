import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Table, Column, ForeignKey

from models import Base

user_group_association_table = Table(
    "user_group_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("user_group_id", ForeignKey("user_group_table.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    groups = relationship(
        "UserGroup", secondary=user_group_association_table, back_populates="users"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id!r}, email={self.email!r}, disabled={self.disabled!r})>"
        )


class UserGroup(Base):
    __tablename__ = "user_group_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]

    users = relationship(
        "User", secondary=user_group_association_table, back_populates="groups"
    )

    def __repr__(self):
        return f"<UserGroup(id={self.id!r}, title={self.title!r}, is_superuser={self.is_superuser!r})>"
