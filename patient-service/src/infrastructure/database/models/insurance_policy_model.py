"""Insurance Policy database model - SQLAlchemy ORM"""
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from infrastructure.database.models.base import Base


class InsurancePolicyModel(Base):
    """Insurance Policy SQLAlchemy model"""

    __tablename__ = "insurance_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # UNIQUE constraint ensures only one policy per patient
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, unique=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("insurance_providers.id", ondelete="RESTRICT"), nullable=False)
    policy_number = Column(String(50), unique=True, nullable=False, index=True)
    coverage_details = Column(String(500), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)

    # Foreign key to catalog table
    status_id = Column(UUID(as_uuid=True), ForeignKey("insurance_statuses.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("PatientModel", back_populates="insurance_policies")
    provider = relationship("InsuranceProviderModel", back_populates="insurance_policies")
    status = relationship("InsuranceStatusModel")

    def __repr__(self):
        return f"<InsurancePolicy(id={self.id}, policy_number={self.policy_number}, status={self.status})>"
