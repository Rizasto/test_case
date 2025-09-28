from datetime import datetime

from passlib.hash import bcrypt

from app.user_data.schema import UserAdd, UserUpdate
from app.db_service.user_data.user_data_repository import UserRepository


class UserAction:
    def __init__(self) -> None:
        self.repository = UserRepository

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.verify(password, hashed)

    def get_user_by_id(self, user_id: int) -> list:
        return self.repository.get_user_by_id(user_id)

    def get_user_by_email(self, user_email: str) -> list:
        return self.repository.get_user_by_email(user_email)

    def register_user(self, user: UserAdd) -> bool:
        if self.repository.get_user_email(user.email):
            return False
        user_password = self.hash_password(user.password)
        user_for_registration = {
            'email': user.email,
            'password_hash': user_password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'is_active': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self.repository.register_user(user_for_registration)
        return True

    def update_info(self, user_id: int, data: UserUpdate) -> None:
        self.repository.update_user_info(user_id, data)

    def delete_user(self, user_id: int) -> None:
        self.repository.delete_user(user_id)


