"""Database models - SQLAlchemy ORM models"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Association table for many-to-many relationship between users and roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False)
)


class RoleModel(Base):
    """SQLAlchemy model for Role entity"""

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to users
    users = relationship("UserModel", secondary=user_roles, back_populates="roles")

    def __repr__(self):
        return f"<RoleModel(id={self.id}, code={self.code}, name={self.name})>"


class UserModel(Base):
    """SQLAlchemy model for User entity"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    national_id_number = Column(String(10), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(10), nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String(30), nullable=False)
    username = Column(String(15), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationship to roles
    roles = relationship("RoleModel", secondary=user_roles, back_populates="users")

    def __repr__(self):
        return f"<UserModel(id={self.id}, username={self.username}, national_id_number={self.national_id_number})>"
