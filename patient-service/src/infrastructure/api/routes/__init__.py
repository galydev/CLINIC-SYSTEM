"""API routes package"""
from infrastructure.api.routes.patient_routes import router as patient_router
from infrastructure.api.routes.emergency_contact_routes import router as emergency_contact_router
from infrastructure.api.routes.insurance_policy_routes import router as insurance_policy_router

__all__ = [
    "patient_router",
    "emergency_contact_router",
    "insurance_policy_router",
]
