"""Patient entity - Core domain model"""
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Patient:

    id: UUID
    national_id_number: str
    full_name: str
    birth_date: date
    gender: str  # Gender code (e.g., 'MALE', 'FEMALE', 'OTHER')
    blood_type: Optional[str]  # Blood type code (e.g., 'A_POSITIVE', 'O_NEGATIVE')
    marital_status: str  # Marital status code (e.g., 'SINGLE', 'MARRIED')
    phone: str
    email: str
    address: str
    occupation: Optional[str]
    allergies: List[str]
    chronic_conditions: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        national_id_number: str,
        full_name: str,
        birth_date: date,
        gender: str,
        marital_status: str,
        phone: str,
        email: str,
        address: str,
        blood_type: Optional[str] = None,
        occupation: Optional[str] = None,
        allergies: Optional[List[str]] = None,
        chronic_conditions: Optional[List[str]] = None
    ) -> "Patient":
        
        # Validate all inputs
        Patient._validate_national_id_number(national_id_number)
        Patient._validate_full_name(full_name)
        Patient._validate_birth_date(birth_date)
        Patient._validate_phone(phone)
        Patient._validate_email(email)
        Patient._validate_address(address)
        if occupation:
            Patient._validate_occupation(occupation)

        now = datetime.utcnow()
        return Patient(
            id=uuid4(),
            national_id_number=national_id_number,
            full_name=full_name,
            birth_date=birth_date,
            gender=gender,
            blood_type=blood_type,
            marital_status=marital_status,
            phone=phone,
            email=email.lower(),
            address=address,
            occupation=occupation,
            allergies=allergies or [],
            chronic_conditions=chronic_conditions or [],
            is_active=True,
            created_at=now,
            updated_at=now
        )

    @staticmethod
    def _validate_national_id_number(national_id_number: str) -> None:
        """Validate national ID number (6-10 digits)"""
        if not national_id_number:
            raise ValueError("National ID number cannot be empty")
        if not national_id_number.isdigit():
            raise ValueError("National ID number must contain only digits")
        if len(national_id_number) < 6 or len(national_id_number) > 10:
            raise ValueError("National ID number must be between 6 and 10 digits")

    @staticmethod
    def _validate_full_name(full_name: str) -> None:
        if not full_name:
            raise ValueError("Full name cannot be empty")
        if len(full_name) > 100:
            raise ValueError("Full name must not exceed 100 characters")

    @staticmethod
    def _validate_birth_date(birth_date: date) -> None:
        """Validate birth date (max 150 years old)"""
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if birth_date > today:
            raise ValueError("Birth date cannot be in the future")
        if age > 150:
            raise ValueError("Age cannot exceed 150 years")
        if age < 0:
            raise ValueError("Invalid birth date")

    @staticmethod
    def _validate_phone(phone: str) -> None:
        """Validate phone number (7-15 digits)"""
        if not phone:
            raise ValueError("Phone cannot be empty")
        if not phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(phone) < 7 or len(phone) > 15:
            raise ValueError("Phone must be between 7 and 15 digits")

    @staticmethod
    def _validate_email(email: str) -> None:
        if not email:
            raise ValueError("Email cannot be empty")
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")

    @staticmethod
    def _validate_address(address: str) -> None:
        if not address:
            raise ValueError("Address cannot be empty")
        if len(address) > 200:
            raise ValueError("Address must not exceed 200 characters")

    @staticmethod
    def _validate_occupation(occupation: str) -> None:
        if occupation and len(occupation) > 100:
            raise ValueError("Occupation must not exceed 100 characters")

    def update_profile(
        self,
        full_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        marital_status: Optional[str] = None,
        occupation: Optional[str] = None
    ) -> None:

        if full_name:
            self._validate_full_name(full_name)
            self.full_name = full_name

        if phone:
            self._validate_phone(phone)
            self.phone = phone

        if email:
            self._validate_email(email)
            self.email = email.lower()

        if address:
            self._validate_address(address)
            self.address = address

        if marital_status:
            self.marital_status = marital_status

        if occupation is not None:
            if occupation:
                self._validate_occupation(occupation)
            self.occupation = occupation

        self.updated_at = datetime.utcnow()

    def add_allergy(self, allergy: str) -> None:
        if not allergy:
            raise ValueError("Allergy cannot be empty")
        if allergy not in self.allergies:
            self.allergies.append(allergy)
            self.updated_at = datetime.utcnow()

    def remove_allergy(self, allergy: str) -> None:
        if allergy in self.allergies:
            self.allergies.remove(allergy)
            self.updated_at = datetime.utcnow()

    def add_chronic_condition(self, condition: str) -> None:
        if not condition:
            raise ValueError("Chronic condition cannot be empty")
        if condition not in self.chronic_conditions:
            self.chronic_conditions.append(condition)
            self.updated_at = datetime.utcnow()

    def remove_chronic_condition(self, condition: str) -> None:
        if condition in self.chronic_conditions:
            self.chronic_conditions.remove(condition)
            self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def get_age(self) -> int:
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        return age

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "national_id_number": self.national_id_number,
            "full_name": self.full_name,
            "birth_date": self.birth_date.isoformat(),
            "age": self.get_age(),
            "gender": self.gender,
            "blood_type": self.blood_type,
            "marital_status": self.marital_status,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "occupation": self.occupation,
            "allergies": self.allergies,
            "chronic_conditions": self.chronic_conditions,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
