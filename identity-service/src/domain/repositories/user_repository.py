"""User repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.user import User


class UserRepository(ABC):
    """Abstract repository interface for User entity"""

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_national_id_number(self, national_id_number: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, national_id_number: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_national_id_number(self, national_id_number: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        pass

    @abstractmethod
    async def assign_role(self, user_id: UUID, role_id: UUID) -> User:
        pass

    @abstractmethod
    async def remove_role(self, user_id: UUID, role_id: UUID) -> User:
        pass
