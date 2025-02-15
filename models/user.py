import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base, user_group_association_table
from mappers import groups_to_list_mapper


class DBUser(Base):
    __tablename__ = "user_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    groups = relationship(
        "DBUserGroup", secondary=user_group_association_table, back_populates="users"
    )

    def __repr__(self):
        return f"<DBUser(id={self.id!r}, email={self.email!r}, disabled={self.disabled!r}, groups={groups_to_list_mapper(self.groups)!r})>"
