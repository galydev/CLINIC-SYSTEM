"""Role entity - Core domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Role:
    id: UUID
    name: str
    code: str  # Unique identifier (e.g., "DOCTOR", "NURSE")
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        name: str,
        code: str,
        description: Optional[str] = None
    ) -> "Role":
        """
        Factory method to create a new role

        Args:
            name: Display name of the role (e.g., "Doctor")
            code: Unique code identifier (e.g., "DOCTOR")
            description: Optional description of the role

        Returns:
            New Role instance
        """
        now = datetime.utcnow()
        return Role(
            id=uuid4(),
            name=name,
            code=code.upper(),
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now
        )

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def update_info(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        if name:
            self.name = name
        if description is not None:
            self.description = description
        self.updated_at = datetime.utcnow()
