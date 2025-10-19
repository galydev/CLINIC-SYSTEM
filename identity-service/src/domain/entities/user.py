"""User entity - Core domain model"""
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class User:
    
    id: UUID
    national_id_number: str
    full_name: str
    email: str
    phone: str
    birth_date: date
    address: str
    username: str
    hashed_password: str
    role_ids: List[UUID]
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    @staticmethod
    def create(
        national_id_number: str,
        full_name: str,
        email: str,
        phone: str,
        birth_date: date,
        address: str,
        username: str,
        hashed_password: str,
        role_ids: Optional[List[UUID]] = None,
        is_superuser: bool = False
    ) -> "User":

        # Validate inputs
        User._validate_national_id_number(national_id_number)
        User._validate_email(email)
        User._validate_phone(phone)
        User._validate_birth_date(birth_date)
        User._validate_address(address)
        User._validate_username(username)

        now = datetime.utcnow()
        return User(
            id=uuid4(),
            national_id_number=national_id_number,
            full_name=full_name,
            email=email.lower(),
            phone=phone,
            birth_date=birth_date,
            address=address,
            username=username,
            hashed_password=hashed_password,
            role_ids=role_ids or [],
            is_active=True,
            is_superuser=is_superuser,
            created_at=now,
            updated_at=now,
            last_login=None
        )

    @staticmethod
    def _validate_national_id_number(national_id_number: str) -> None:
        if not national_id_number:
            raise ValueError("National ID number cannot be empty")
        if not national_id_number.isdigit():
            raise ValueError("National ID number must contain only digits")
        if len(national_id_number) > 10:
            raise ValueError("National ID number must not exceed 10 digits")
        if len(national_id_number) < 6:
            raise ValueError("National ID number must have at least 6 digits")

    @staticmethod
    def _validate_email(email: str) -> None:
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")

    @staticmethod
    def _validate_phone(phone: str) -> None:
        if not phone:
            raise ValueError("Phone cannot be empty")
        if not phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(phone) < 1 or len(phone) > 10:
            raise ValueError("Phone must be between 1 and 10 digits")

    @staticmethod
    def _validate_birth_date(birth_date: date) -> None:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if birth_date > today:
            raise ValueError("Birth date cannot be in the future")
        if age > 150:
            raise ValueError("Age cannot exceed 150 years")
        if age < 0:
            raise ValueError("Invalid birth date")

    @staticmethod
    def _validate_address(address: str) -> None:
        if not address:
            raise ValueError("Address cannot be empty")
        if len(address) > 30:
            raise ValueError("Address must not exceed 30 characters")

    @staticmethod
    def _validate_username(username: str) -> None:
        if not username:
            raise ValueError("Username cannot be empty")
        if len(username) > 15:
            raise ValueError("Username must not exceed 15 characters")
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValueError("Username must contain only letters and numbers")

    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate password strength

        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one number
        - At least one special character

        Args:
            password: Plain text password to validate

        Raises:
            ValueError: If password doesn't meet requirements
        """
        if not password:
            raise ValueError("Password cannot be empty")

        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")

        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must include at least one uppercase letter")

        if not re.search(r'\d', password):
            raise ValueError("Password must include at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;`~]', password):
            raise ValueError("Password must include at least one special character")

    def update_last_login(self) -> None:
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def add_role(self, role_id: UUID) -> None:

        if role_id not in self.role_ids:
            self.role_ids.append(role_id)
            self.updated_at = datetime.utcnow()

    def remove_role(self, role_id: UUID) -> None:

        if role_id in self.role_ids:
            self.role_ids.remove(role_id)
            self.updated_at = datetime.utcnow()

    def has_role(self, role_id: UUID) -> bool:

        return role_id in self.role_ids

    def to_dict(self) -> Dict:

        return {
            "id": str(self.id),
            "national_id_number": self.national_id_number,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date.isoformat(),
            "address": self.address,
            "username": self.username,
            "role_ids": [str(role_id) for role_id in self.role_ids],
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

    def update_profile(
        self,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ) -> None:
        
        if full_name:
            self.full_name = full_name

        if email:
            self._validate_email(email)
            self.email = email.lower()

        if phone:
            self._validate_phone(phone)
            self.phone = phone

        if address:
            self._validate_address(address)
            self.address = address

        self.updated_at = datetime.utcnow()
