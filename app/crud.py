from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List  # Added import for List
from app.models import User
from app.schemas import UserCreate, UserUpdate
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user(user: UserCreate, db: Session) -> User | None:
    """
    Create a new user in the database.

    Args:
        user: UserCreate schema with user details (email, name, age).
        db: Database session.

    Returns:
        User object if created successfully, None if email already exists.

    Raises:
        HTTPException: If database operation fails or email exists.
    """
    try:
        # Check for existing user with the same email
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        # Create new user
        new_user = User(email=user.email, name=user.name, age=user.age)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"Created user with ID: {new_user.id}")
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def get_user(user_id: int, db: Session) -> User | None:
    """
    Retrieve a user by ID.

    Args:
        user_id: ID of the user to retrieve.
        db: Database session.

    Returns:
        User object if found, None otherwise.
    """
    try:
        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            logger.info(f"Retrieved user with ID: {user_id}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def update_user(user_id: int, user: UserUpdate, db: Session) -> User | None:
    """
    Update an existing user's details.

    Args:
        user_id: ID of the user to update.
        user: UserUpdate schema with updated fields.
        db: Database session.

    Returns:
        Updated User object if found, None otherwise.

    Raises:
        HTTPException: If database operation fails or input is invalid.
    """
    try:
        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        # Check for email uniqueness if email is being updated
        if user.email and user.email != db_user.email:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        # Update fields
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Updated user with ID: {user_id}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def delete_user(user_id: int, db: Session) -> bool:
    """
    Delete a user by ID.

    Args:
        user_id: ID of the user to delete.
        db: Database session.

    Returns:
        True if user was deleted, False if user not found.

    Raises:
        HTTPException: If database operation fails or input is invalid.
    """
    try:
        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        db.delete(db_user)
        db.commit()
        logger.info(f"Deleted user with ID: {user_id}")
        return True
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def get_all_users(db: Session) -> List[User]:
    """
    Retrieve all users from the database.

    Args:
        db: Database session.

    Returns:
        List of User objects.

    Raises:
        HTTPException: If database operation fails.
    """
    try:
        users = db.query(User).all()
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Failed to retrieve users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )