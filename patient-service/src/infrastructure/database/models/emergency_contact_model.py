"""Emergency Contact database model - SQLAlchemy ORM"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from infrastructure.database.models.base import Base


class EmergencyContactModel(Base):
    """Emergency Contact SQLAlchemy model"""

    __tablename__ = "emergency_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)

    # Foreign key to catalog table
    relationship_type_id = Column(UUID(as_uuid=True), ForeignKey("relationship_types.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("PatientModel", back_populates="emergency_contacts")
    relationship_type = relationship("RelationshipTypeModel")

    def __repr__(self):
        return f"<EmergencyContact(id={self.id}, name={self.full_name}, relationship={self.relationship_type})>"
