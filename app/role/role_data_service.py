from app.role.schema import CreatePermission
from app.db_service.role.role_data_repository import RoleRepository


class RoleActions:
    def __init__(self) -> None:
        self.repository = RoleRepository

    def get_permissions(self, user_id: int) -> list:
        return self.repository.get_permissions(user_id)

    def check_permission(self, permission: str, user_id: int) -> bool:
        permissions = self.get_permissions(user_id)
        if permission not in permissions:
            return False
        return True

    def get_role(self, user_id: int) -> str:
        return self.repository.get_role(user_id).code

    def create_permission(self, permission: CreatePermission) -> None:
        self.repository.create_permission(permission)

    def assign_permission(self, permission_code: str, role_code: str) -> None:
        self.repository.assign_permission(permission_code, role_code)

    def get_all_permissions(self) -> dict:
        unique_roles = {}
        permissions = self.repository.get_all_permissions()
        for item in permissions:
            if item.name not in unique_roles:
                unique_roles[item.name] = []
                unique_roles[item.name].append(item.code)
            else:
                unique_roles[item.name].append(item.code)
        return unique_roles
