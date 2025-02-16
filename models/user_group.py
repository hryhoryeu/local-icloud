import uuid
from typing import TYPE_CHECKING

from sqlalchemy import orm as so
import sqlalchemy as sa

from models.base import Base, user_group_association_table

if TYPE_CHECKING:
    from models.user import DBUser


class DBUserGroup(Base):
    __tablename__ = "user_group_table"

    id: so.Mapped[uuid.UUID] = so.mapped_column(primary_key=True, default=uuid.uuid4)
    title: so.Mapped[str]

    users: so.Mapped[list["DBUser"]] = so.relationship(
        "DBUser",
        secondary=user_group_association_table,
        back_populates="groups",
    )

    __table_args__ = (sa.UniqueConstraint("title", name="uq_group_title"),)

    def __repr__(self):
        return f"<DBUserGroup(id={self.id!r}, title={self.title!r})>"
