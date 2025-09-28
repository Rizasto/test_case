from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from datetime import datetime
from app.db_service.session import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=False)
    middle_name = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    code = Column(Text, nullable=False)


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False, primary_key=True)


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id = Column(Integer, ForeignKey(Role.id), nullable=False, primary_key=True)
    permission_id = Column(Integer, ForeignKey(Permission.id), nullable=False, primary_key=True)
