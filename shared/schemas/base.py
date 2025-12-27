"""
Base Pydantic schemas with common fields.

All API schemas should inherit from these base classes.
This ensures consistency across all services.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class BaseSchema(BaseModel):
    """
    Base schema with common configuration.

    Features:
    - Converts ORM models to dicts automatically
    - Validates data types
    - Generates JSON schema
    """

    model_config = ConfigDict(
        from_attributes=True,  # Allow creating from ORM models
        populate_by_name=True,  # Allow field aliases
        str_strip_whitespace=True,  # Strip whitespace from strings
        json_schema_extra={
            "example": {}  # Can override in child classes
        }
    )


class TimestampSchema(BaseSchema):
    """
    Schema with timestamp fields.

    Use this for responses that include creation/update times.
    """
    created_at: datetime = Field(
        ...,
        description="Timestamp when the record was created"
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the record was last updated"
    )


class IDSchema(BaseSchema):
    """
    Schema with ID field.

    Use this for responses that include a unique identifier.
    """
    id: UUID = Field(
        ...,
        description="Unique identifier"
    )


class BaseDBSchema(IDSchema, TimestampSchema):
    """
    Complete base schema for database models.

    Includes:
    - id (UUID)
    - created_at (datetime)
    - updated_at (datetime)

    Example:
        class UserResponse(BaseDBSchema):
            email: str
            role: str
            # id, created_at, updated_at automatically included!
    """
    pass


class PaginationParams(BaseSchema):
    """
    Pagination query parameters.

    Use this for list endpoints.

    Example:
        @app.get("/users")
        async def list_users(
            pagination: PaginationParams = Depends()
        ):
            skip = (pagination.page - 1) * pagination.page_size
            # Query database with skip and limit
    """
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (starts from 1)"
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page (max 100)"
    )


class PaginatedResponse(BaseSchema):
    """
    Paginated response wrapper.

    Example:
        class UserListResponse(PaginatedResponse):
            items: List[UserResponse]
    """
    total: int = Field(
        ...,
        description="Total number of items"
    )
    page: int = Field(
        ...,
        description="Current page number"
    )
    page_size: int = Field(
        ...,
        description="Items per page"
    )
    total_pages: int = Field(
        ...,
        description="Total number of pages"
    )


class ErrorResponse(BaseSchema):
    """
    Standard error response.

    All API errors should return this format.

    Example:
        {
            "detail": "User not found",
            "code": "USER_NOT_FOUND",
            "field": "user_id"  # optional
        }
    """
    detail: str = Field(
        ...,
        description="Human-readable error message"
    )
    code: Optional[str] = Field(
        None,
        description="Machine-readable error code"
    )
    field: Optional[str] = Field(
        None,
        description="Field that caused the error (for validation errors)"
    )


class SuccessResponse(BaseSchema):
    """
    Standard success response for operations without data.

    Example:
        return SuccessResponse(message="User deleted successfully")
    """
    message: str = Field(
        ...,
        description="Success message"
    )