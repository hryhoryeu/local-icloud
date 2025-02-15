from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import orm as so

from schemas.user_group import UserGroup, UserGroupResponse
from database import get_db
from services.user_group import UserGroupService
from auth.permissions import HasAny
from auth.user import login_required
from constants import Groups

router = APIRouter(
    prefix="/user-group",
    tags=["User Group"],
    dependencies=[Depends(login_required), Depends(HasAny(Groups.ADMIN.value))],
)


@router.post(
    "/create",
    responses={status.HTTP_409_CONFLICT: {"description": "User Group already exists"}},
    status_code=status.HTTP_201_CREATED,
)
async def create_user_group(
    user_group: UserGroup, db: Annotated[so.Session, Depends(get_db)]
) -> UserGroupResponse:
    return UserGroupService(db=db).add(entity=user_group)


@router.get("/list")
async def get_all_user_groups(db: Annotated[so.Session, Depends(get_db)]):
    return UserGroupService(db=db).get_all()
