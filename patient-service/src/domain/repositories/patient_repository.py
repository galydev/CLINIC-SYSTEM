"""Patient repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.patient import Patient


class PatientRepository(ABC):

    @abstractmethod
    async def save(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    async def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        pass

    @abstractmethod
    async def get_by_national_id_number(self, national_id_number: str) -> Optional[Patient]:
        pass

    @abstractmethod
    async def update(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    async def delete(self, patient_id: UUID) -> bool:
        pass

    @abstractmethod
    async def exists_by_national_id_number(self, national_id_number: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        pass

    @abstractmethod
    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Patient]:
        pass
