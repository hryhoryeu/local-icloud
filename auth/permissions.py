from abc import ABC

import structlog
from fastapi import Request

from auth.models import User
from errors import PermissionDenied
from settings import secrets

logger = structlog.getLogger(__name__)


class PermissionDependency(ABC):
    def __init__(self) -> None:
        pass

    def get_user(self, *, request: Request) -> User:
        return request.state.user


class HasAny(PermissionDependency):
    def __init__(self, *permissions: str) -> None:
        self.permissions = permissions
        if secrets.DEBUG:
            self.permissions += ("Superuser",)

    def __call__(self, request: Request) -> None:
        for permission in self.permissions:
            if self.get_user(request=request).has_permission(permission=permission):
                logger.debug("User has permission '%s'", permission)
                return

        logger.debug("Permission denied")
        raise PermissionDenied(detail="Permission denied")
