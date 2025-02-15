from fastapi.security import HTTPBearer
from pydantic.dataclasses import dataclass

HTTP_BEARER = HTTPBearer()


@dataclass(frozen=True)
class Token:
    access_token: str
