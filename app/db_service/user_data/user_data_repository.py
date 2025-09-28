from app.user_data.schema import UserUpdate
from app.db_service.models import User
from app.db_service.session import DBSession


class UserRepository:

    @staticmethod
    def register_user(user: dict) -> None:
        try:
            DBSession.add(User(**user))
            DBSession.commit()
        except:
            DBSession.rollback()

    @staticmethod
    def get_user_email(user_email: str) -> list:
        return DBSession.query(User).filter(User.email == user_email).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> list:
        return DBSession.query(User.id,
                               User.email,
                               User.password_hash,
                               User.is_active
                               ).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(user_email: str) -> list:
        return DBSession.query(User.id,
                               User.email,
                               User.password_hash,
                               User.is_active).filter(User.email == user_email).first()

    @staticmethod
    def update_user_info(user_id: int, data: UserUpdate) -> None:
        try:
            user = DBSession.query(User).filter(User.id == user_id).first()
            if user:
                user.first_name = data.first_name if data.first_name else user.first_name,
                user.last_name = data.last_name if data.last_name else user.last_name,
                user.middle_name = data.middle_name if data.middle_name else user.middle_name
                DBSession.commit()
        except:
            DBSession.rollback()

    @staticmethod
    def delete_user(user_id: int) -> None:
        try:
            user = DBSession.query(User).filter(User.id == user_id).first()
            if user:
                user.is_active = False
                DBSession.commit()
        except:
            DBSession.rollback()

