"""Role repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.role import Role


class RoleRepository(ABC):
    """Abstract repository interface for Role entity"""

    @abstractmethod
    async def create(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def save(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Role]:
        pass

    @abstractmethod
    async def update(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def delete(self, code: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_code(self, code: str) -> bool:
        pass

    @abstractmethod
    async def get_user_roles(self, user_id: UUID) -> List[Role]:
        pass
