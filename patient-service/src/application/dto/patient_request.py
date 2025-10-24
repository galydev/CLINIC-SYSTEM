from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterPatientRequest(BaseModel):

    national_id_number: str = Field(..., min_length=6, max_length=10, pattern=r'^\d+$')
    full_name: str = Field(..., min_length=1, max_length=100)
    birth_date: date
    gender: str = Field(..., description="Gender code (e.g., 'MALE', 'FEMALE', 'OTHER')")
    marital_status: str = Field(..., description="Marital status code (e.g., 'SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED', 'SEPARATED')")
    phone: str = Field(..., min_length=7, max_length=15, pattern=r'^\d+$')
    email: EmailStr
    address: str = Field(..., min_length=1, max_length=200)
    blood_type: Optional[str] = Field(None, description="Blood type code (e.g., 'A_POSITIVE', 'O_NEGATIVE')")
    occupation: Optional[str] = Field(None, max_length=100)
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None

    @field_validator('gender', 'marital_status', 'blood_type')
    @classmethod
    def validate_uppercase(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.upper()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "national_id_number": "1234567890",
                "full_name": "John Doe",
                "birth_date": "1990-01-15",
                "gender": "MALE",
                "marital_status": "SINGLE",
                "phone": "1234567890",
                "email": "john.doe@example.com",
                "address": "123 Main St, City, Country",
                "blood_type": "O+",
                "occupation": "Software Engineer",
                "allergies": ["Penicillin"],
                "chronic_conditions": ["Diabetes"]
            }
        }


class UpdatePatientRequest(BaseModel):

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=15, pattern=r'^\d+$')
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    marital_status: Optional[str] = Field(None, description="Marital status code (e.g., 'SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED', 'SEPARATED')")
    occupation: Optional[str] = Field(None, max_length=100)

    @field_validator('marital_status')
    @classmethod
    def validate_uppercase(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.upper()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Updated Doe",
                "phone": "9876543210",
                "email": "john.updated@example.com",
                "address": "456 New St, City, Country",
                "marital_status": "MARRIED",
                "occupation": "Senior Engineer"
            }
        }
