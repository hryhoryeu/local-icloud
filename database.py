from typing import Generator
import sqlalchemy as sa
from sqlalchemy import orm as so

from settings import secrets

engine = sa.create_engine(secrets.generate_db_url())

SessionLocal = so.sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[so.Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
