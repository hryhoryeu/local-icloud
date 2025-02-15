from enum import Enum

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
LOOKER_GROUP_ID = "b7b9fd57-6fb7-42c6-874c-19584d815842"


class Groups(Enum):
    SUPERUSER = "Superuser"
    ADMIN = "Admin"
    LOOKER = "Looker"
