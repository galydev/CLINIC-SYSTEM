"""Insurance Status catalog model"""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.database.models.base import Base, TimestampMixin
import uuid


class InsuranceStatusModel(Base, TimestampMixin):
    """Insurance Status catalog table"""
    __tablename__ = "insurance_statuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True, nullable=False)
