import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base, user_group_association_table


class DBUserGroup(Base):
    __tablename__ = "user_group_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(unique=True)

    users = relationship(
        "DBUser", secondary=user_group_association_table, back_populates="groups"
    )

    def __repr__(self):
        return f"<DBUserGroup(id={self.id!r}, title={self.title!r})>"
