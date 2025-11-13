from dishka import Provider, Scope, provide

from maxhack.database.repos.event import EventRepo
from maxhack.database.repos.group import GroupRepo
from maxhack.database.repos.invite import InviteRepo
from maxhack.database.repos.respond import RespondRepo
from maxhack.database.repos.role import RoleRepo
from maxhack.database.repos.tag import TagRepo
from maxhack.database.repos.user import UserRepo
from maxhack.database.repos.users_to_groups import UsersToGroupsRepo


class ReposProvider(Provider):
    scope = Scope.REQUEST

    user_repo = provide(UserRepo)
    group_repo = provide(GroupRepo)
    invite_repo = provide(InviteRepo)
    users_to_groups_repo = provide(UsersToGroupsRepo)
    tag_repo = provide(TagRepo)
    event_repo = provide(EventRepo)
    respond_repo = provide(RespondRepo)
    role_repo = provide(RoleRepo)
