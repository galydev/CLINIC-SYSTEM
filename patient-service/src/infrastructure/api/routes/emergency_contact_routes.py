"""Emergency Contact API routes"""
from uuid import UUID

from application.dto import (AddEmergencyContactRequest,
                             EmergencyContactResponse)
from application.dto.error_response import ErrorResponse
from application.use_cases.add_emergency_contact import (
    AddEmergencyContactUseCase, PatientNotFoundError, ValidationError)
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.api.dependencies import (
    get_add_emergency_contact_use_case, get_emergency_contact_repository)

router = APIRouter(prefix="/patients/{patient_id}/emergency-contacts", tags=["Emergency Contacts"])


@router.post(
    "/",
    response_model=EmergencyContactResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        404: {"model": ErrorResponse, "description": "Not Found - Patient not found"}
    },
    summary="Add emergency contact to patient",
    description="Add a new emergency contact to a patient's record with contact information and relationship"
)
async def add_emergency_contact(
    patient_id: UUID,
    request: AddEmergencyContactRequest,
    use_case: AddEmergencyContactUseCase = Depends(get_add_emergency_contact_use_case)
):

    try:
        return await use_case.execute(patient_id, request)
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/",
    response_model=list[EmergencyContactResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all emergency contacts for patient",
    description="Retrieve all emergency contacts associated with a patient"
)
async def get_emergency_contacts(
    patient_id: UUID,
    emergency_contact_repository = Depends(get_emergency_contact_repository)
):

    try:
        contacts = await emergency_contact_repository.get_by_patient_id(patient_id)

        return [
            EmergencyContactResponse(
                id=contact.id,
                patient_id=contact.patient_id,
                full_name=contact.full_name,
                phone=contact.phone,
                relationship=contact.relationship,
                created_at=contact.created_at,
                updated_at=contact.updated_at
            )
            for contact in contacts
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
