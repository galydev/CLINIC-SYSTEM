"""Relationship type enumeration"""
from enum import Enum


class RelationshipType(str, Enum):
    """Types of relationships for emergency contacts"""
    SPOUSE = "SPOUSE"
    PARENT = "PARENT"
    CHILD = "CHILD"
    SIBLING = "SIBLING"
    FRIEND = "FRIEND"
    OTHER = "OTHER"
