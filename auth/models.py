from abc import ABC


class AuthUser(ABC):
    pass


class User(AuthUser):
    def __init__(self, *, email: str, groups: list[str]) -> None:
        self.email = email
        self.groups = groups

    def has_permission(self, *, permission) -> bool:
        return permission in self.groups


class SuperUser(User):
    def __init__(self) -> None:
        self.email = "super@user.com"
        self.groups = ["Superuser"]
