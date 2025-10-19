"""Role repository implementation - SQLAlchemy implementation"""
import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.role import Role
from domain.repositories.role_repository import RoleRepository
from infrastructure.database.models import RoleModel, UserModel

# Configure logger
logger = logging.getLogger(__name__)


class RoleRepositoryImpl(RoleRepository):
    """
    SQLAlchemy implementation of RoleRepository

    This class implements the RoleRepository interface using SQLAlchemy ORM
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

    def _to_entity(self, model: RoleModel) -> Role:
        """
        Convert SQLAlchemy model to domain entity

        Args:
            model: RoleModel database model

        Returns:
            Role domain entity
        """
        return Role(
            id=model.id,
            name=model.name,
            code=model.code,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Role) -> RoleModel:
        """
        Convert domain entity to SQLAlchemy model

        Args:
            entity: Role domain entity

        Returns:
            RoleModel database model
        """
        return RoleModel(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def save(self, role: Role) -> Role:
        """
        Save a role (create or update)

        Args:
            role: Role entity to save

        Returns:
            Saved role entity

        Raises:
            ValueError: If role code already exists
            Exception: If database operation fails
        """
        try:
            logger.info(f"Saving role with code: {role.code}")

            model = self._to_model(role)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

            logger.info(f"Successfully saved role with code: {role.code}")
            return self._to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error saving role {role.code}: {e}")
            raise ValueError(f"Role with code '{role.code}' already exists")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error saving role {role.code}: {e}")
            raise Exception(f"Failed to save role: {e}")

    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Get role by ID

        Args:
            role_id: UUID of the role

        Returns:
            Role entity if found, None otherwise
        """
        try:
            logger.debug(f"Getting role by ID: {role_id}")

            result = await self.session.execute(
                select(RoleModel).where(RoleModel.id == role_id)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found role with ID: {role_id}")
                return self._to_entity(model)

            logger.debug(f"Role not found with ID: {role_id}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting role by ID {role_id}: {e}")
            raise Exception(f"Failed to get role by ID: {e}")

    async def get_by_code(self, code: str) -> Optional[Role]:
        """
        Get role by code

        Args:
            code: Role's unique code

        Returns:
            Role entity if found, None otherwise
        """
        try:
            logger.debug(f"Getting role by code: {code}")

            result = await self.session.execute(
                select(RoleModel).where(RoleModel.code == code)
            )
            model = result.scalar_one_or_none()

            if model:
                logger.debug(f"Found role with code: {code}")
                return self._to_entity(model)

            logger.debug(f"Role not found with code: {code}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error getting role by code {code}: {e}")
            raise Exception(f"Failed to get role by code: {e}")

    async def update(self, role: Role) -> Role:
        """
        Update an existing role

        Args:
            role: Role entity with updated data

        Returns:
            Updated role entity

        Raises:
            ValueError: If role doesn't exist
            Exception: If database operation fails
        """
        try:
            logger.info(f"Updating role with code: {role.code}")

            result = await self.session.execute(
                select(RoleModel).where(RoleModel.code == role.code)
            )
            model = result.scalar_one_or_none()

            if not model:
                logger.warning(f"Role not found for update: {role.code}")
                raise ValueError(f"Role with code {role.code} not found")

            # Update fields
            model.name = role.name
            model.description = role.description
            model.is_active = role.is_active
            model.updated_at = role.updated_at

            await self.session.commit()
            await self.session.refresh(model)

            logger.info(f"Successfully updated role with code: {role.code}")
            return self._to_entity(model)

        except ValueError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error updating role {role.code}: {e}")
            raise Exception(f"Failed to update role: {e}")

    async def delete(self, code: str) -> bool:
        """
        Delete a role by code

        Args:
            code: Role's unique code

        Returns:
            True if role was deleted, False if role not found

        Raises:
            Exception: If database operation fails
        """
        try:
            logger.info(f"Deleting role with code: {code}")

            result = await self.session.execute(
                select(RoleModel).where(RoleModel.code == code)
            )
            model = result.scalar_one_or_none()

            if not model:
                logger.warning(f"Role not found for deletion: {code}")
                return False

            await self.session.delete(model)
            await self.session.commit()

            logger.info(f"Successfully deleted role with code: {code}")
            return True

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error deleting role {code}: {e}")
            raise Exception(f"Failed to delete role: {e}")

    async def exists_by_code(self, code: str) -> bool:
        """
        Check if role exists by code

        Args:
            code: Role's unique code

        Returns:
            True if role exists, False otherwise
        """
        try:
            logger.debug(f"Checking if role exists by code: {code}")

            result = await self.session.execute(
                select(RoleModel.id).where(RoleModel.code == code)
            )
            exists = result.scalar_one_or_none() is not None

            logger.debug(f"Role exists by code {code}: {exists}")
            return exists

        except SQLAlchemyError as e:
            logger.error(f"Database error checking role existence by code {code}: {e}")
            raise Exception(f"Failed to check role existence: {e}")

    async def create(self, role: Role) -> Role:
        """
        Create a new role

        Args:
            role: Role entity to create

        Returns:
            Created role entity

        Raises:
            ValueError: If role code already exists
            Exception: If database operation fails
        """
        try:
            logger.info(f"Creating new role with code: {role.code}")

            # Check if role already exists
            if await self.exists_by_code(role.code):
                raise ValueError(f"Role with code '{role.code}' already exists")

            model = self._to_model(role)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

            logger.info(f"Successfully created role with code: {role.code}")
            return self._to_entity(model)

        except ValueError:
            await self.session.rollback()
            raise
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error creating role {role.code}: {e}")
            raise ValueError(f"Role with code '{role.code}' already exists")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error creating role {role.code}: {e}")
            raise Exception(f"Failed to create role: {e}")

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Role]:
        """
        Get all roles with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            only_active: If True, return only active roles

        Returns:
            List of role entities
        """
        try:
            logger.debug(f"Getting all roles (skip={skip}, limit={limit}, only_active={only_active})")

            query = select(RoleModel)

            if only_active:
                query = query.where(RoleModel.is_active == True)

            query = query.offset(skip).limit(limit).order_by(RoleModel.name)

            result = await self.session.execute(query)
            models = result.scalars().all()

            logger.debug(f"Found {len(models)} roles")
            return [self._to_entity(model) for model in models]

        except SQLAlchemyError as e:
            logger.error(f"Database error getting all roles: {e}")
            raise Exception(f"Failed to get all roles: {e}")

    async def get_user_roles(self, user_id: UUID) -> List[Role]:
        """
        Get all roles assigned to a user

        Args:
            user_id: UUID of the user

        Returns:
            List of role entities assigned to the user
        """
        try:
            logger.debug(f"Getting roles for user: {user_id}")

            result = await self.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.roles))
                .where(UserModel.id == user_id)
            )
            user_model = result.scalar_one_or_none()

            if not user_model:
                logger.debug(f"User not found: {user_id}")
                return []

            roles = [self._to_entity(role_model) for role_model in user_model.roles]
            logger.debug(f"Found {len(roles)} roles for user {user_id}")
            return roles

        except SQLAlchemyError as e:
            logger.error(f"Database error getting roles for user {user_id}: {e}")
            raise Exception(f"Failed to get user roles: {e}")
