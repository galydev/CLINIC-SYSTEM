from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AddEmergencyContactRequest(BaseModel):

    full_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=7, max_length=15, pattern=r'^\d+$')
    relationship: str = Field(..., description="Relationship type code (e.g., 'SPOUSE', 'PARENT', 'CHILD', 'SIBLING', 'FRIEND', 'OTHER')")

    @field_validator('relationship')
    @classmethod
    def validate_uppercase(cls, v: str) -> str:
        return v.upper()

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "phone": "9876543210",
                "relationship": "SPOUSE"
            }
        }


class UpdateEmergencyContactRequest(BaseModel):

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=15, pattern=r'^\d+$')
    relationship: Optional[str] = Field(None, description="Relationship type code (e.g., 'SPOUSE', 'PARENT', 'CHILD', 'SIBLING', 'FRIEND', 'OTHER')")

    @field_validator('relationship')
    @classmethod
    def validate_uppercase(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.upper()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Jane Updated Doe",
                "phone": "1112223333",
                "relationship": "PARENT"
            }
        }
