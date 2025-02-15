from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Table, Column, ForeignKey


class Base(DeclarativeBase):
    pass


user_group_association_table = Table(
    "user_group_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("user_group_id", ForeignKey("user_group_table.id"), primary_key=True),
    extend_existing=True,
)
