import uuid

from pydantic import BaseModel, EmailStr, ConfigDict

from schemas.user_group import UserGroupResponse


class UserBase(BaseModel):
    email: EmailStr
    disabled: bool = False


class User(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID
    groups: list[UserGroupResponse]

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserForm(BaseModel):
    email: EmailStr
    password: str
