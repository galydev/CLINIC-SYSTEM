"""Emergency Contact entity - Core domain model"""
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from uuid import UUID, uuid4


@dataclass
class EmergencyContact:
    """
    Emergency contact information for a patient.

    Relationship is stored as a string code to allow dynamic catalog values.
    """

    id: UUID
    patient_id: UUID
    full_name: str
    phone: str
    relationship: str  # Relationship type code (e.g., 'SPOUSE', 'PARENT', 'CHILD')
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        patient_id: UUID,
        full_name: str,
        phone: str,
        relationship: str
    ) -> "EmergencyContact":
        """
        Create a new emergency contact

        Args:
            patient_id: UUID of the patient
            full_name: Full name of the contact
            phone: Phone number
            relationship: Relationship type code (e.g., 'SPOUSE', 'PARENT')

        Returns:
            EmergencyContact instance

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        EmergencyContact._validate_full_name(full_name)
        EmergencyContact._validate_phone(phone)

        now = datetime.utcnow()
        return EmergencyContact(
            id=uuid4(),
            patient_id=patient_id,
            full_name=full_name,
            phone=phone,
            relationship=relationship,
            created_at=now,
            updated_at=now
        )

    @staticmethod
    def _validate_full_name(full_name: str) -> None:
        """Validate full name"""
        if not full_name:
            raise ValueError("Full name cannot be empty")
        if len(full_name) > 100:
            raise ValueError("Full name must not exceed 100 characters")

    @staticmethod
    def _validate_phone(phone: str) -> None:
        """Validate phone number"""
        if not phone:
            raise ValueError("Phone cannot be empty")
        if not phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(phone) < 7 or len(phone) > 15:
            raise ValueError("Phone must be between 7 and 15 digits")

    def update(
        self,
        full_name: str = None,
        phone: str = None,
        relationship: str = None
    ) -> None:
        """
        Update emergency contact information

        Args:
            full_name: New full name (optional)
            phone: New phone (optional)
            relationship: New relationship type code (optional, e.g., 'SIBLING')
        """
        if full_name:
            self._validate_full_name(full_name)
            self.full_name = full_name

        if phone:
            self._validate_phone(phone)
            self.phone = phone

        if relationship:
            self.relationship = relationship

        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "id": str(self.id),
            "patient_id": str(self.patient_id),
            "full_name": self.full_name,
            "phone": self.phone,
            "relationship": self.relationship,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
