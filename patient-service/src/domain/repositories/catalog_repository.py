"""Catalog repository interfaces"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class GenderRepository(ABC):

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[UUID]:
        pass


class BloodTypeRepository(ABC):

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[UUID]:
        pass


class MaritalStatusRepository(ABC):

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[UUID]:
        pass


class RelationshipTypeRepository(ABC):

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[UUID]:
        pass


class InsuranceStatusRepository(ABC):

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[UUID]:
        pass
