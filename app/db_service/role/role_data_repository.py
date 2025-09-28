from app.role.schema import CreatePermission
from app.db_service.models import Permission, Role, RolePermission, UserRole
from app.db_service.session import DBSession


class RoleRepository:

    @staticmethod
    def get_permissions(user_id: int) -> list:
        permissions = (DBSession.query(Permission.code)
                       .join(RolePermission, Permission.id == RolePermission.permission_id)
                       .join(Role, Role.id == RolePermission.role_id)
                       .join(UserRole, Role.id == UserRole.role_id)
                       .filter(UserRole.user_id == user_id).all())
        return [permission.code for permission in permissions]

    @staticmethod
    def get_role(user_id: int) -> list:
        return (DBSession.query(Role.code)
                .join(UserRole, Role.id == UserRole.role_id)
                .filter(UserRole.user_id == user_id).first())

    @staticmethod
    def create_permission(permission: CreatePermission) -> None:
        DBSession.add(Permission(code=permission.code))
        DBSession.commit()

    @staticmethod
    def assign_permission(permission_code: str, role_code: str) -> None:
        permission_id = DBSession.query(Permission.id).filter(Permission.code == permission_code).first().id
        role_id = DBSession.query(Role.id).filter(Role.code == role_code).first().id
        DBSession.add(RolePermission(role_id=role_id, permission_id=permission_id))
        DBSession.commit()

    @staticmethod
    def get_all_permissions() -> list:
        return (DBSession.query(Role.name,
                                Permission.code)
                .join(RolePermission, Role.id == RolePermission.role_id)
                .join(Permission, Permission.id == RolePermission.permission_id)
                .join(UserRole, Role.id == UserRole.role_id).all())
