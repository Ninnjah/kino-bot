from typing import Union, Collection, Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.when import Predicate, Whenable

from tgbot.models.role import UserRole


class RoleFilter(Predicate):
    def __init__(self, role: Union[UserRole, Collection[UserRole]]) -> None:
        if isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    def __call__(
        self,
        data: Dict,
        widget: Whenable,
        dialog_manager: DialogManager,
    ) -> bool:
        roles = dialog_manager.middleware_data["roles"]
        return any((role for role in roles if role in self.roles))


class IsAdminFilter(RoleFilter):
    def __init__(self) -> None:
        super().__init__([UserRole.ADMIN, UserRole.SUDO])


class IsSudoFilter(RoleFilter):
    def __init__(self) -> None:
        super().__init__(UserRole.SUDO)
