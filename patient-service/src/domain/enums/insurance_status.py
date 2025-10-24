"""Insurance status enumeration"""
from enum import Enum


class InsuranceStatus(str, Enum):
    """Insurance policy status options"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    EXPIRED = "EXPIRED"
