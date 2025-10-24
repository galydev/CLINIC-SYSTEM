"""Patient database model - SQLAlchemy ORM"""
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from infrastructure.database.models.base import Base


class PatientModel(Base):
    """Patient SQLAlchemy model"""

    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id_number = Column(String(10), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)

    # Foreign keys to catalog tables
    gender_id = Column(UUID(as_uuid=True), ForeignKey("genders.id"), nullable=False)
    blood_type_id = Column(UUID(as_uuid=True), ForeignKey("blood_types.id"), nullable=True)
    marital_status_id = Column(UUID(as_uuid=True), ForeignKey("marital_statuses.id"), nullable=False)

    phone = Column(String(15), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    address = Column(String(200), nullable=False)
    occupation = Column(String(100), nullable=True)
    allergies = Column(ARRAY(String), default=list)
    chronic_conditions = Column(ARRAY(String), default=list)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships to catalog tables
    gender = relationship("GenderModel")
    blood_type = relationship("BloodTypeModel")
    marital_status = relationship("MaritalStatusModel")

    # Relationships to other entities
    emergency_contacts = relationship(
        "EmergencyContactModel",
        back_populates="patient",
        cascade="all, delete-orphan"
    )
    insurance_policies = relationship(
        "InsurancePolicyModel",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Patient(id={self.id}, national_id={self.national_id_number}, name={self.full_name})>"
