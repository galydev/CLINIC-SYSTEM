"""Gender enumeration"""
from enum import Enum


class Gender(str, Enum):
    """Gender options for patients"""
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
