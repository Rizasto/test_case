from app.db_service.session import DBSession
from app.db_service.models import *
from app.user_data.user_data_service import UserAction

user_admin = User(id=1,
                  email='admin@admin.com',
                  password_hash=UserAction().hash_password('12345'),
                  first_name='admin',
                  last_name='admin',
                  middle_name='admin')

user_moderator = User(id=2,
                      email='moderator@moderator.com',
                      password_hash=UserAction().hash_password('12345'),
                      first_name='moderator',
                      last_name='moderator',
                      middle_name='moderator')

user_user = User(id=3,
                 email='user@user.com',
                 password_hash=UserAction().hash_password('12345'),
                 first_name='user',
                 last_name='user',
                 middle_name='user')

role_admin = Role(id=1,
                  code='admin',
                  name='Администратор')

role_moderator = Role(id=2,
                      code='moderator',
                      name='Модератор')

role_user = Role(id=3,
                 code='user',
                 name='Пользователь')

permissions = [{'id': 1, 'code': 'get_all_products'},
               {'id': 2, 'code': 'get_my_products'},
               {'id': 3, 'code': 'update_my_products'},
               {'id': 4, 'code': 'update_all_products'}]

user_roles = [{'user_id': 1, 'role_id': 1},
              {'user_id': 2, 'role_id': 2},
              {'user_id': 3, 'role_id': 3}]

role_permissions = [{'role_id': 1, 'permission_id': 1},
                    {'role_id': 1, 'permission_id': 2},
                    {'role_id': 1, 'permission_id': 3},
                    {'role_id': 1, 'permission_id': 4},
                    {'role_id': 2, 'permission_id': 1},
                    {'role_id': 2, 'permission_id': 2},
                    {'role_id': 2, 'permission_id': 3},
                    {'role_id': 2, 'permission_id': 4},
                    {'role_id': 3, 'permission_id': 2},
                    {'role_id': 3, 'permission_id': 3}]


def run():
    DBSession.add_all([user_admin, user_moderator, user_user])
    DBSession.add_all([role_admin, role_moderator, role_user])
    DBSession.add_all([Permission(**permission) for permission in permissions])
    DBSession.add_all([UserRole(**user_role) for user_role in user_roles])
    DBSession.add_all([RolePermission(**role_permission) for role_permission in role_permissions])
    DBSession.commit()


if __name__ == '__main__':
    run()
