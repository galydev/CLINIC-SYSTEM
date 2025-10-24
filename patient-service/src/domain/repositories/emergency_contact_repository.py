"""Emergency Contact repository interface - Domain layer contract"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.emergency_contact import EmergencyContact


class EmergencyContactRepository(ABC):

    @abstractmethod
    async def save(self, emergency_contact: EmergencyContact) -> EmergencyContact:
        pass

    @abstractmethod
    async def get_by_id(self, contact_id: UUID) -> Optional[EmergencyContact]:
        pass

    @abstractmethod
    async def get_by_patient_id(self, patient_id: UUID) -> List[EmergencyContact]:
        pass

    @abstractmethod
    async def update(self, emergency_contact: EmergencyContact) -> EmergencyContact:
        pass

    @abstractmethod
    async def delete(self, contact_id: UUID) -> bool:
        pass
