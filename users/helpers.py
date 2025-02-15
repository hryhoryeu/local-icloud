from typing import Annotated
from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
import sqlalchemy as sa
from sqlalchemy import orm as so
from fastapi import Depends
from fastapi.security import HTTPBearer
import jwt

from database import engine
from schemas.user import UserInDB, UserResponse
from models.user import DBUser
from settings import secrets
from errors import UnauthorizedError, BadRequestError
from constants import ALGORITHM


security = HTTPBearer()


def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    ph = PasswordHasher()
    return ph.verify(hashed_password, plain_password)


def get_user(email: str) -> UserInDB:
    with so.Session(engine) as session:
        user = session.execute(sa.select(DBUser).filter(DBUser.email == email)).scalar()
    return UserInDB.model_validate(user)


def authenticate_user(email: str, password: str) -> UserResponse:
    user = get_user(email)
    if not user:
        return False
    if not verify_password(user.hashed_password, password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: Annotated[str, Depends(security)]):
    credential_exception = UnauthorizedError(detail="Could not validate credentials")
    try:
        payload = jwt.decode(
            credentials.credentials, secrets.SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
    except jwt.exceptionsInvalidTokenError:
        raise credential_exception
    user = get_user(email=email)
    import ipdb

    ipdb.set_trace()
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserResponse:
    if current_user.disabled:
        raise BadRequestError(detail="Inactive user.")
    return UserResponse(**current_user.model_dump())
