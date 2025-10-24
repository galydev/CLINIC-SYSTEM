"""Insurance Policy API routes"""
from uuid import UUID

from application.dto import (AddInsurancePolicyRequest,
                             InsurancePolicyResponse, InsuranceStatusResponse)
from application.dto.error_response import ErrorResponse
from application.use_cases.add_insurance_policy import (
    AddInsurancePolicyUseCase, DuplicatePolicyError,
    InsuranceProviderNotFoundError)
from application.use_cases.add_insurance_policy import \
    PatientNotFoundError as AddPolicyPatientNotFoundError
from application.use_cases.add_insurance_policy import ValidationError
from application.use_cases.get_insurance_status import \
    GetInsuranceStatusUseCase
from application.use_cases.get_insurance_status import \
    PatientNotFoundError as GetStatusPatientNotFoundError
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.api.dependencies import (get_add_insurance_policy_use_case,
                                             get_get_insurance_status_use_case,
                                             get_insurance_policy_repository)

router = APIRouter(prefix="/patients/{patient_id}/insurance-policies", tags=["Insurance Policies"])


@router.post(
    "/",
    response_model=InsurancePolicyResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        404: {"model": ErrorResponse, "description": "Not Found - Patient or insurance provider not found"},
        409: {"model": ErrorResponse, "description": "Conflict - Insurance policy already exists or patient already has a policy"}
    },
    summary="Add insurance policy to patient",
    description="Add a new insurance policy to a patient's record with provider information and coverage details"
)
async def add_insurance_policy(
    patient_id: UUID,
    request: AddInsurancePolicyRequest,
    use_case: AddInsurancePolicyUseCase = Depends(get_add_insurance_policy_use_case)
):
    try:
        return await use_case.execute(patient_id, request)
    except AddPolicyPatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InsuranceProviderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicatePolicyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
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
    response_model=list[InsurancePolicyResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all insurance policies for patient",
    description="Retrieve all insurance policies associated with a patient, including active and expired policies"
)
async def get_insurance_policies(
    patient_id: UUID,
    insurance_policy_repository = Depends(get_insurance_policy_repository)
):
    try:
        policies = await insurance_policy_repository.get_by_patient_id(patient_id)

        return [
            InsurancePolicyResponse(
                id=policy.id,
                patient_id=policy.patient_id,
                provider_id=policy.provider_id,
                policy_number=policy.policy_number,
                coverage_details=policy.coverage_details,
                valid_from=policy.valid_from,
                valid_until=policy.valid_until,
                status=policy.status,
                created_at=policy.created_at,
                updated_at=policy.updated_at
            )
            for policy in policies
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/status",
    response_model=InsuranceStatusResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Not Found - Patient not found"}
    },
    summary="Get insurance status for patient",
    description="Get the current insurance status for a patient, including active policies and coverage information"
)
async def get_insurance_status(
    patient_id: UUID,
    use_case: GetInsuranceStatusUseCase = Depends(get_get_insurance_status_use_case)
):
    try:
        return await use_case.execute(patient_id)
    except GetStatusPatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
