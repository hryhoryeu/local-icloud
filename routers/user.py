from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import orm as so

from schemas.user import User, UserResponse
from services.user import UserService
from database import get_db
from auth.user import login_required
from auth.permissions import HasAny
from constants import Groups

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(login_required), Depends(HasAny(Groups.ADMIN.value))],
)


@router.post(
    "/create",
    responses={status.HTTP_409_CONFLICT: {"description": "User already exists"}},
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: User, db: Annotated[so.Session, Depends(get_db)]):
    return UserService(db=db).add(entity=user)


@router.get("/list")
async def get_users(db: Annotated[so.Session, Depends(get_db)]):
    return UserService(db=db).get_all()


@router.get("/get")
async def get_by_email(
    email: str, db: Annotated[so.Session, Depends(get_db)]
) -> UserResponse:
    return UserService(db=db).get_by_email(email=email)
