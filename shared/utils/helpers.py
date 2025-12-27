"""
Common utility functions used across services.
"""

from typing import Optional, TypeVar, Generic
from datetime import datetime, timedelta
import secrets
import string
from uuid import UUID, uuid4

T = TypeVar('T')


def generate_uuid() -> UUID:
    """Generate a new UUID4."""
    return uuid4()


def generate_random_string(length: int = 32) -> str:
    """
    Generate a cryptographically secure random string.

    Args:
        length: Length of the string (default 32)

    Returns:
        Random string containing letters and digits

    Example:
        api_key = generate_random_string(64)
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_api_key() -> str:
    """
    Generate an API key with prefix.

    Format: aimpk_<64 random characters>

    Returns:
        API key string

    Example:
        key = generate_api_key()
        # Returns: "aimpk_a1b2c3d4..."
    """
    random_part = generate_random_string(64)
    return f"aimpk_{random_part}"


def get_expiry_time(days: Optional[int] = None, hours: Optional[int] = None) -> datetime:
    """
    Calculate expiry datetime from now.

    Args:
        days: Number of days from now
        hours: Number of hours from now

    Returns:
        Expiry datetime

    Example:
        expiry = get_expiry_time(days=30)  # 30 days from now
    """
    now = datetime.utcnow()

    if days:
        return now + timedelta(days=days)
    elif hours:
        return now + timedelta(hours=hours)
    else:
        return now + timedelta(days=30)  # Default 30 days


def is_expired(expiry_time: datetime) -> bool:
    """
    Check if a datetime has passed.

    Args:
        expiry_time: Datetime to check

    Returns:
        True if expired, False otherwise
    """
    return datetime.utcnow() > expiry_time


class Paginator(Generic[T]):
    """
    Helper class for pagination.

    Example:
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        paginator = Paginator(items, page=2, page_size=3)

        print(paginator.items)  # [4, 5, 6]
        print(paginator.total_pages)  # 4
        print(paginator.has_next)  # True
    """

    def __init__(self, items: list[T], page: int, page_size: int):
        self.all_items = items
        self.page = page
        self.page_size = page_size
        self.total = len(items)
        self.total_pages = (self.total + page_size - 1) // page_size

        # Calculate slice indices
        start = (page - 1) * page_size
        end = start + page_size

        self.items = items[start:end]

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1