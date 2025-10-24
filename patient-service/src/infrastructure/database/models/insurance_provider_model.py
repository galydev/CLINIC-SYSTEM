"""Insurance Provider database model - SQLAlchemy ORM"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from infrastructure.database.models.base import Base


class InsuranceProviderModel(Base):
    """Insurance Provider SQLAlchemy model"""

    __tablename__ = "insurance_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    address = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    insurance_policies = relationship("InsurancePolicyModel", back_populates="provider")

    def __repr__(self):
        return f"<InsuranceProvider(id={self.id}, name={self.name}, code={self.code})>"
