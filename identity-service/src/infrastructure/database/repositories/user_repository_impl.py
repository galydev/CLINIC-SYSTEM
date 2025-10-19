"""User repository implementation - SQLAlchemy implementation"""
import logging
from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.database.models import RoleModel, UserModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Configure logger
logger = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    """
    SQLAlchemy implementation of UserRepository

    This class implements the UserRepository interface using SQLAlchemy ORM
    with PostgreSQL. It handles conversion between domain entities and database models,
    includes proper transaction management, exception handling, and logging.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize repository with database session

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """
        Convert SQLAlchemy model to domain entity

        Args:
            model: UserModel database model

        Returns:
            User domain entity
        """
        # Extract role IDs from the relationship
        role_ids = [role.id for role in model.roles] if model.roles else []

        return User(
            id=model.id,
            national_id_number=model.national_id_number,
            full_name=model.full_name,
            email=model.email,
            phone=model.phone,
            birth_date=model.birth_date,
            address=model.address,
            username=model.username,
            hashed_password=model.hashed_password,
            role_ids=role_ids,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login
        )

    def _to_model(self, entity: User) -> UserModel:
        """
        Convert domain entity to SQLAlchemy model

        Args:
            entity: User domain entity

        Returns:
            UserModel database model

        Note:
            This method does NOT set the roles relationship.
            Use _sync_roles() to manage role associations.
        """
        return UserModel(
            id=entity.id,
            national_id_number=entity.national_id_number,
            full_name=entity.full_name,
            email=entity.email,
            phone=entity.phone,
            birth_date=entity.birth_date,
            address=entity.address,
            username=entity.username,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_login=entity.last_login
        )

    async def _sync_roles(self, model: UserModel, role_ids: list[UUID]) -> None:
        """
        Synchronize user roles in database

        Args:
            model: UserModel to update
            role_ids: List of role UUIDs to assign
        """
        # Clear existing roles
        model.roles.clear()

        # Add new roles
        if role_ids:
            result = await self.session.execute(
                select(RoleModel).where(RoleModel.id.in_(role_ids))
            )
            roles = result.scalars().all()
            model.roles.extend(roles)

    async def save(self, user: User) -> User:
        """
        Save a user (create or update)

        Args:
            user: User entity to save

        Returns:
            Saved user entity

        Raises:
            IntegrityError: If cedula, email, or username already exists
            SQLAlchemyError: If database operation fails
        """
        try:
            logger.info(f"Saving user with national_id_number: {user.national_id_number}")

            # Convert entity to model
            model = self._to_model(user)

            # Add to session
            self.session.add(model)

            # Sync roles
            await self._sync_roles(model, user.role_ids)

            # Commit transaction
            await self.session.commit()
            await self.session.refresh(model, ["roles"])

            logger.info(f"Successfully saved user with national_id_number: {user.national_id_number}")
            return self._to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error saving user {user.national_id_number}: {e}")
            raise ValueError(f"User with national_id_number, email, or username already exists: {e}")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error saving user {user.national_id_number}: {e}")
            raise Exception(f"Failed to save user: {e}")

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User's UUID as string

        Returns:
            User entity if found, None otherwise
        """
        try:
            from uuid import UUID
            logger.debug(f"Getting user by ID: {user_id}")

            # Convert string to UUID
            try:
                uuid_obj = UUID(user_id)
            except (ValueError, AttributeError) as e:
                logger.warning(f"Invalid UUID format: {user_id}")
                return None

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.id == uuid_obj)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found user with ID: {user_id}")
                return self._to_entity(model)

            logger.debug(f"User not found with ID: {user_id}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by ID {user_id}: {e}")
            raise Exception(f"Failed to get user by ID: {e}")

    async def get_by_national_id_number(self, national_id_number: str) -> Optional[User]:
        try:
            logger.debug(f"Getting user by national_id_number: {national_id_number}")

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.national_id_number == national_id_number)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found user with national_id_number: {national_id_number}")
                return self._to_entity(model)

            logger.debug(f"User not found with national_id_number: {national_id_number}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by national_id_number {national_id_number}: {e}")
            raise Exception(f"Failed to get user by national_id_number: {e}")

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username

        Args:
            username: User's username

        Returns:
            User entity if found, None otherwise
        """
        try:
            logger.debug(f"Getting user by username: {username}")

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.username == username)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found user with username: {username}")
                return self._to_entity(model)

            logger.debug(f"User not found with username: {username}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by username {username}: {e}")
            raise Exception(f"Failed to get user by username: {e}")

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: User's email

        Returns:
            User entity if found, None otherwise
        """
        try:
            logger.debug(f"Getting user by email: {email}")

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.email == email)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found user with email: {email}")
                return self._to_entity(model)

            logger.debug(f"User not found with email: {email}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting user by email {email}: {e}")
            raise Exception(f"Failed to get user by email: {e}")

    async def update(self, user: User) -> User:
        """
        Update an existing user

        Args:
            user: User entity with updated data

        Returns:
            Updated user entity

        Raises:
            ValueError: If user doesn't exist
            SQLAlchemyError: If database operation fails
        """
        try:
            logger.info(f"Updating user with national_id_number: {user.national_id_number}")

            # Get existing user
            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.national_id_number == user.national_id_number)
            )
            model = result.scalar_one_or_none()

            if not model:
                logger.warning(f"User not found for update: {user.national_id_number}")
                raise ValueError(f"User with national_id_number {user.national_id_number} not found")

            # Update fields
            model.full_name = user.full_name
            model.email = user.email
            model.phone = user.phone
            model.birth_date = user.birth_date
            model.address = user.address
            model.username = user.username
            model.hashed_password = user.hashed_password
            model.is_active = user.is_active
            model.is_superuser = user.is_superuser
            model.updated_at = user.updated_at
            model.last_login = user.last_login

            # Sync roles
            await self._sync_roles(model, user.role_ids)

            # Commit transaction
            await self.session.commit()
            await self.session.refresh(model, ["roles"])

            logger.info(f"Successfully updated user with national_id_number: {user.national_id_number}")
            return self._to_entity(model)

        except ValueError:
            await self.session.rollback()
            raise
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error updating user {user.national_id_number}: {e}")
            raise ValueError(f"Email or username already exists: {e}")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error updating user {user.national_id_number}: {e}")
            raise Exception(f"Failed to update user: {e}")

    async def delete(self, national_id_number: str) -> bool:
        """
        Delete a user by national ID number

        Args:
            national_id_number: User's national ID number

        Returns:
            True if user was deleted, False if user not found

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            logger.info(f"Deleting user with national_id_number: {national_id_number}")

            result = await self.session.execute(
                select(UserModel).where(UserModel.national_id_number == national_id_number)
            )
            model = result.scalar_one_or_none()

            if not model:
                logger.warning(f"User not found for deletion: {national_id_number}")
                return False

            await self.session.delete(model)
            await self.session.commit()

            logger.info(f"Successfully deleted user with national_id_number: {national_id_number}")
            return True

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error deleting user {national_id_number}: {e}")
            raise Exception(f"Failed to delete user: {e}")

    async def exists_by_national_id_number(self, national_id_number: str) -> bool:
        """
        Check if user exists by national ID number

        Args:
            national_id_number: User's national ID number

        Returns:
            True if user exists, False otherwise
        """
        try:
            logger.debug(f"Checking if user exists by national_id_number: {national_id_number}")

            result = await self.session.execute(
                select(UserModel.id).where(UserModel.national_id_number == national_id_number)
            )
            exists = result.scalar_one_or_none() is not None

            logger.debug(f"User exists by national_id_number {national_id_number}: {exists}")
            return exists

        except SQLAlchemyError as e:
            logger.error(f"Database error checking user existence by national_id_number {national_id_number}: {e}")
            raise Exception(f"Failed to check user existence: {e}")

    async def exists_by_username(self, username: str) -> bool:
        """
        Check if user exists by username

        Args:
            username: User's username

        Returns:
            True if user exists, False otherwise
        """
        try:
            logger.debug(f"Checking if user exists by username: {username}")

            result = await self.session.execute(
                select(UserModel.id).where(UserModel.username == username)
            )
            exists = result.scalar_one_or_none() is not None

            logger.debug(f"User exists by username {username}: {exists}")
            return exists

        except SQLAlchemyError as e:
            logger.error(f"Database error checking user existence by username {username}: {e}")
            raise Exception(f"Failed to check user existence: {e}")

    async def exists_by_email(self, email: str) -> bool:
        """
        Check if user exists by email

        Args:
            email: User's email

        Returns:
            True if user exists, False otherwise
        """
        try:
            logger.debug(f"Checking if user exists by email: {email}")

            result = await self.session.execute(
                select(UserModel.id).where(UserModel.email == email)
            )
            exists = result.scalar_one_or_none() is not None

            logger.debug(f"User exists by email {email}: {exists}")
            return exists

        except SQLAlchemyError as e:
            logger.error(f"Database error checking user existence by email {email}: {e}")
            raise Exception(f"Failed to check user existence: {e}")

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Get all users with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of user entities
        """
        try:
            logger.debug(f"Getting all users (skip={skip}, limit={limit})")

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .offset(skip)
                .limit(limit)
                .order_by(UserModel.created_at.desc())
            )
            models = result.scalars().all()

            users = [self._to_entity(model) for model in models]
            logger.debug(f"Found {len(users)} users")
            return users

        except SQLAlchemyError as e:
            logger.error(f"Database error getting all users: {e}")
            raise Exception(f"Failed to get all users: {e}")

    async def assign_role(self, user_id: UUID, role_id: UUID) -> User:
        """
        Assign a role to a user

        Args:
            user_id: UUID of the user
            role_id: UUID of the role to assign

        Returns:
            Updated user entity with the new role

        Raises:
            ValueError: If user or role not found, or role already assigned
        """
        try:
            logger.info(f"Assigning role {role_id} to user {user_id}")

            # Get user with roles loaded
            user_result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.id == user_id)
            )
            user_model = user_result.scalar_one_or_none()

            if not user_model:
                logger.warning(f"User not found: {user_id}")
                raise ValueError(f"User with ID {user_id} not found")

            # Get role
            role_result = await self.session.execute(
                select(RoleModel).where(RoleModel.id == role_id)
            )
            role_model = role_result.scalar_one_or_none()

            if not role_model:
                logger.warning(f"Role not found: {role_id}")
                raise ValueError(f"Role with ID {role_id} not found")

            # Check if role is already assigned
            if role_model in user_model.roles:
                logger.warning(f"Role {role_id} already assigned to user {user_id}")
                raise ValueError(f"Role {role_model.code} is already assigned to this user")

            # Assign role
            user_model.roles.append(role_model)
            await self.session.commit()
            await self.session.refresh(user_model, ["roles"])

            logger.info(f"Successfully assigned role {role_id} to user {user_id}")
            return self._to_entity(user_model)

        except ValueError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error assigning role {role_id} to user {user_id}: {e}")
            raise Exception(f"Failed to assign role: {e}")

    async def remove_role(self, user_id: UUID, role_id: UUID) -> User:
        """
        Remove a role from a user

        Args:
            user_id: UUID of the user
            role_id: UUID of the role to remove

        Returns:
            Updated user entity without the role

        Raises:
            ValueError: If user or role not found, or role not assigned
        """
        try:
            logger.info(f"Removing role {role_id} from user {user_id}")

            # Get user with roles loaded
            user_result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.id == user_id)
            )
            user_model = user_result.scalar_one_or_none()

            if not user_model:
                logger.warning(f"User not found: {user_id}")
                raise ValueError(f"User with ID {user_id} not found")

            # Get role
            role_result = await self.session.execute(
                select(RoleModel).where(RoleModel.id == role_id)
            )
            role_model = role_result.scalar_one_or_none()

            if not role_model:
                logger.warning(f"Role not found: {role_id}")
                raise ValueError(f"Role with ID {role_id} not found")

            # Check if role is assigned
            if role_model not in user_model.roles:
                logger.warning(f"Role {role_id} not assigned to user {user_id}")
                raise ValueError(f"Role {role_model.code} is not assigned to this user")

            # Remove role
            user_model.roles.remove(role_model)
            await self.session.commit()
            await self.session.refresh(user_model, ["roles"])

            logger.info(f"Successfully removed role {role_id} from user {user_id}")
            return self._to_entity(user_model)

        except ValueError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error removing role {role_id} from user {user_id}: {e}")
            raise Exception(f"Failed to remove role: {e}")
