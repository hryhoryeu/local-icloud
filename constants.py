from enum import Enum

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Groups(Enum):
    SUPERUSER = "Superuser"
    ADMIN = "Admin"
    LOOKER = "Looker"
