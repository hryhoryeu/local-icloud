from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import orm as so

from schemas.user_group import UserGroup, UserGroupResponse
from database import get_db
from services.user_group import UserGroupService

router = APIRouter(prefix="/user-group", tags=["User Group"])


@router.post(
    "/create",
    responses={409: {"description": "User Group already exists"}},
    status_code=status.HTTP_201_CREATED,
)
async def create_user_group(
    user_group: UserGroup, db: Annotated[so.Session, Depends(get_db)]
) -> UserGroupResponse:
    return UserGroupService(db=db).add(entity=user_group)


@router.get("/list")
async def get_all_user_groups(db: Annotated[so.Session, Depends(get_db)]):
    return UserGroupService(db=db).get_all()
