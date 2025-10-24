from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PatientResponse(BaseModel):

    id: UUID
    national_id_number: str
    full_name: str
    birth_date: date
    age: int
    gender: str = Field(..., description="Gender code (e.g., 'MALE', 'FEMALE', 'OTHER')")
    blood_type: Optional[str] = Field(None, description="Blood type code (e.g., 'A_POSITIVE', 'O_NEGATIVE')")
    marital_status: str = Field(..., description="Marital status code (e.g., 'SINGLE', 'MARRIED')")
    phone: str
    email: str
    address: str
    occupation: Optional[str]
    allergies: List[str]
    chronic_conditions: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "national_id_number": "1234567890",
                "full_name": "John Doe",
                "birth_date": "1990-01-15",
                "age": 34,
                "gender": "MALE",
                "blood_type": "O_POSITIVE",
                "marital_status": "SINGLE",
                "phone": "1234567890",
                "email": "john.doe@example.com",
                "address": "123 Main St, City, Country",
                "occupation": "Software Engineer",
                "allergies": ["Penicillin"],
                "chronic_conditions": ["Diabetes"],
                "is_active": True,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
