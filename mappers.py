from schemas.user_group import UserGroupResponse
from models.user_group import DBUserGroup


def groups_to_list_mapper(groups: list[UserGroupResponse | DBUserGroup]) -> list[str]:
    return list(map(lambda x: x.title, groups))
