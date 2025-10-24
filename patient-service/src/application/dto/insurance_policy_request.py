from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class AddInsurancePolicyRequest(BaseModel):

    provider_id: UUID = Field(..., description="UUID of the insurance provider")
    policy_number: str = Field(..., min_length=1, max_length=50)
    coverage_details: str = Field(..., min_length=1, max_length=500)
    valid_from: date
    valid_until: date

    class Config:
        json_schema_extra = {
            "example": {
                "provider_id": "123e4567-e89b-12d3-a456-426614174003",
                "policy_number": "POL-2024-12345",
                "coverage_details": "Full medical coverage including emergency, hospitalization, and outpatient services",
                "valid_from": "2024-01-01",
                "valid_until": "2025-12-31"
            }
        }


class UpdateInsurancePolicyRequest(BaseModel):
    provider_id: UUID = Field(None, description="UUID of the insurance provider")
    coverage_details: str = Field(None, min_length=1, max_length=500)
    valid_from: date = None
    valid_until: date = None

    class Config:
        json_schema_extra = {
            "example": {
                "provider_id": "123e4567-e89b-12d3-a456-426614174003",
                "coverage_details": "Extended coverage including dental and vision",
                "valid_from": "2024-01-01",
                "valid_until": "2026-12-31"
            }
        }
