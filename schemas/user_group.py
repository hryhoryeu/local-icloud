from pydantic import BaseModel, ConfigDict
import uuid


class UserGroupBase(BaseModel):
    title: str


class UserGroup(UserGroupBase):
    pass


class UserGroupResponse(UserGroupBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
