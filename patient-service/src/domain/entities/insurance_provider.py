"""Insurance Provider entity - Core domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID, uuid4


@dataclass
class InsuranceProvider:

    id: UUID
    name: str
    code: str  # Unique identifier code for the provider
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    address: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        name: str,
        code: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        address: Optional[str] = None
    ) -> "InsuranceProvider":
        
        # Validate inputs
        InsuranceProvider._validate_name(name)
        InsuranceProvider._validate_code(code)
        if phone:
            InsuranceProvider._validate_phone(phone)
        if email:
            InsuranceProvider._validate_email(email)
        if website:
            InsuranceProvider._validate_website(website)
        if address:
            InsuranceProvider._validate_address(address)

        current_time = datetime.utcnow()
        return InsuranceProvider(
            id=uuid4(),
            name=name,
            code=code.upper(),
            phone=phone,
            email=email.lower() if email else None,
            website=website,
            address=address,
            is_active=True,
            created_at=current_time,
            updated_at=current_time
        )

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate provider name"""
        if not name:
            raise ValueError("Provider name cannot be empty")
        if len(name) > 100:
            raise ValueError("Provider name must not exceed 100 characters")

    @staticmethod
    def _validate_code(code: str) -> None:
        """Validate provider code"""
        if not code:
            raise ValueError("Provider code cannot be empty")
        if len(code) > 20:
            raise ValueError("Provider code must not exceed 20 characters")
        if not code.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Provider code must be alphanumeric (dashes and underscores allowed)")

    @staticmethod
    def _validate_phone(phone: str) -> None:
        """Validate phone number (7-15 digits)"""
        if not phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(phone) < 7 or len(phone) > 15:
            raise ValueError("Phone must be between 7 and 15 digits")

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format"""
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")

    @staticmethod
    def _validate_website(website: str) -> None:
        """Validate website URL"""
        if len(website) > 200:
            raise ValueError("Website URL must not exceed 200 characters")

    @staticmethod
    def _validate_address(address: str) -> None:
        """Validate address (max 200 characters)"""
        if len(address) > 200:
            raise ValueError("Address must not exceed 200 characters")

    def update_info(
        self,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        address: Optional[str] = None
    ) -> None:
        """
        Update provider information

        Args:
            name: New provider name (optional)
            phone: New phone (optional)
            email: New email (optional)
            website: New website (optional)
            address: New address (optional)
        """
        if name:
            self._validate_name(name)
            self.name = name

        if phone is not None:
            if phone:
                self._validate_phone(phone)
            self.phone = phone

        if email is not None:
            if email:
                self._validate_email(email)
                self.email = email.lower()
            else:
                self.email = None

        if website is not None:
            if website:
                self._validate_website(website)
            self.website = website

        if address is not None:
            if address:
                self._validate_address(address)
            self.address = address

        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the insurance provider"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the insurance provider"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "address": self.address,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
