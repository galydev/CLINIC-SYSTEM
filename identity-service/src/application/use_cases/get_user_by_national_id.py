"""Get user by national ID use case"""
from typing import Optional

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class GetUserByNationalIdUseCase:
    """Use case for retrieving a user by their national ID number"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, national_id_number: str) -> Optional[User]:

        if not national_id_number or not isinstance(national_id_number, str):
            raise ValueError("National ID number must be a non-empty string")

        if not national_id_number.isdigit():
            raise ValueError("National ID number must contain only digits")

        if len(national_id_number) < 6 or len(national_id_number) > 10:
            raise ValueError("National ID number must be 6-10 digits")

        return await self.user_repository.get_by_national_id_number(national_id_number)
