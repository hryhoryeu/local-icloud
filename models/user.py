import uuid
from typing import TYPE_CHECKING

from sqlalchemy import orm as so
import sqlalchemy as sa

from models.base import Base, user_group_association_table
from mappers import groups_to_list_mapper

if TYPE_CHECKING:
    from models.user_group import DBUserGroup


class DBUser(Base):
    __tablename__ = "user_table"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid.uuid4)
    email: so.Mapped[str]
    hashed_password: so.Mapped[str]
    disabled: so.Mapped[bool] = so.mapped_column(default=False)

    groups: so.Mapped[list["DBUserGroup"]] = so.relationship(
        "DBUserGroup", secondary=user_group_association_table, back_populates="users"
    )

    __table_args__ = (sa.UniqueConstraint("email", name="uq_user_email"),)

    def __repr__(self):
        return f"<DBUser(id={self.id!r}, email={self.email!r}, disabled={self.disabled!r}, groups={groups_to_list_mapper(self.groups)!r})>"
