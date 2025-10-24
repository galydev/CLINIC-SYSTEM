"""Patient API routes"""
from uuid import UUID

from application.dto import (PatientResponse, RegisterPatientRequest,
                             UpdatePatientRequest)
from application.dto.error_response import ErrorResponse
from application.use_cases.get_patient import GetPatientUseCase
from application.use_cases.get_patient import \
    PatientNotFoundError as GetPatientNotFoundError
from application.use_cases.register_patient import (DuplicatePatientError,
                                                    RegisterPatientUseCase)
from application.use_cases.register_patient import \
    ValidationError as RegisterValidationError
from application.use_cases.update_patient import (PatientNotFoundError,
                                                  UpdatePatientUseCase)
from application.use_cases.update_patient import \
    ValidationError as UpdateValidationError
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.api.dependencies import (get_get_patient_use_case,
                                             get_register_patient_use_case,
                                             get_update_patient_use_case)

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        409: {"model": ErrorResponse, "description": "Conflict - Patient already exists"}
    },
    summary="Register a new patient",
    description="Create a new patient record with personal information, medical history, and allergies"
)
async def register_patient(
    request: RegisterPatientRequest,
    use_case: RegisterPatientUseCase = Depends(get_register_patient_use_case)
):

    try:
        return await use_case.execute(request)
    except DuplicatePatientError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except RegisterValidationError as e:
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
    "/{patient_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Not Found - Patient not found"}
    },
    summary="Get patient by ID",
    description="Retrieve a patient's complete information including medical history and allergies by their UUID"
)
async def get_patient_by_id(
    patient_id: UUID,
    use_case: GetPatientUseCase = Depends(get_get_patient_use_case)
):

    try:
        return await use_case.execute_by_id(patient_id)
    except GetPatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/national-id/{national_id_number}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Not Found - Patient not found"}
    },
    summary="Get patient by national ID number",
    description="Retrieve a patient's information by their national ID number (cedula)"
)
async def get_patient_by_national_id(
    national_id_number: str,
    use_case: GetPatientUseCase = Depends(get_get_patient_use_case)
):

    try:
        return await use_case.execute_by_national_id(national_id_number)
    except GetPatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        404: {"model": ErrorResponse, "description": "Not Found - Patient not found"}
    },
    summary="Update patient information",
    description="Update patient's personal information, contact details, and medical data"
)
async def update_patient(
    patient_id: UUID,
    request: UpdatePatientRequest,
    use_case: UpdatePatientUseCase = Depends(get_update_patient_use_case)
):

    try:
        return await use_case.execute(patient_id, request)
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UpdateValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
