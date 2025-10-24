from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EmergencyContactResponse(BaseModel):

    id: UUID
    patient_id: UUID
    full_name: str
    phone: str
    relationship: str = Field(..., description="Relationship type code (e.g., 'SPOUSE', 'PARENT', 'CHILD')")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "full_name": "Jane Doe",
                "phone": "9876543210",
                "relationship": "SPOUSE",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
