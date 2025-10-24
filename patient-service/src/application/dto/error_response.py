from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Patient not found",
                "detail": "The requested patient does not exist",
                "code": "PATIENT_001"
            }
        }