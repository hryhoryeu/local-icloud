from pydantic import BaseModel, EmailStr, ConfigDict
import uuid


class UserBase(BaseModel):
    email: EmailStr
    is_superuser: bool = False
    disabled: bool = False


class User(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserForm(BaseModel):
    email: EmailStr
    password: str
