"""Marital status enumeration"""
from enum import Enum


class MaritalStatus(str, Enum):
    """Marital status options"""
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"
    SEPARATED = "SEPARATED"
