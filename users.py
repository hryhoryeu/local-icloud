from argon2 import PasswordHasher
import sqlalchemy as sa
from sqlalchemy import orm as so
from database import engine, User
from models import UserInDB, UserResponse
import jwt
from jwt.exceptions import InvalidTokenError
from settings import secrets
from datetime import datetime, timedelta, timezone
from errors import UnauthorizedError, BadRequestError, PermissionDenied
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from typing import Annotated
from constants import ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    ph = PasswordHasher()
    return ph.verify(hashed_password, plain_password)


def get_user(email: str) -> UserInDB:
    with so.Session(engine) as session:
        user = session.execute(sa.select(User).filter(User.email == email)).scalar()
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
    except InvalidTokenError:
        raise credential_exception
    user = get_user(email=email)
    import ipdb

    ipdb.set_trace()
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    if current_user.disabled:
        raise BadRequestError(detail="Inactive user.")
    return UserResponse(**current_user.model_dump())


async def is_superuser(user: Annotated[UserResponse, Depends(get_current_active_user)]):
    if not user.is_superuser:
        raise PermissionDenied(detail=f"{user.email} is not superuser.")
