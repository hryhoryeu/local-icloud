from typing import Annotated

from datetime import datetime, timedelta, timezone
from sqlalchemy import orm as so
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from argon2 import PasswordHasher

from auth.tokens import HTTP_BEARER
from errors import UnauthorizedError
from settings import secrets
from constants import ALGORITHM
from schemas.user import UserInDB
from services.user import UserService
from errors import InvalidTokenError
from auth.models import User, SuperUser


def login_required(
    request: Request,
    http_bearer: Annotated[HTTPAuthorizationCredentials, Depends(HTTP_BEARER)],
) -> None:
    if secrets.DEBUG:
        user = SuperUser()
        request.state.user = user
        return

    if not http_bearer:
        raise UnauthorizedError(detail="Unauthenticated")

    token = http_bearer.credentials

    try:
        payload = jwt.decode(token, secrets.SECRET_KEY, algorithms=[ALGORITHM])
        user = User(email=payload.get("sub"), groups=payload.get("groups"))
        request.state.user = user
    except jwt.DecodeError as exc:
        raise InvalidTokenError(detail="Invalid token") from exc


def verify_password(hashed_password: str, plain_password: str) -> bool:
    ph = PasswordHasher()
    return ph.verify(hashed_password, plain_password)


def authenticate_user(*, email: str, password: str, db: so.Session) -> UserInDB:
    user = UserService(db=db).get_by_email(email=email)
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
