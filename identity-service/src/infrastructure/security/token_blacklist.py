"""Token Blacklist - In-memory storage for invalidated tokens"""
from datetime import datetime, timedelta
from typing import Set
import threading


class TokenBlacklist:
    """
    In-memory token blacklist for logout functionality

    Note: In production, use Redis or a database for persistence
    across multiple instances and restarts.
    """

    def __init__(self):
        """Initialize the blacklist with thread-safe set"""
        self._blacklist: Set[str] = set()
        self._lock = threading.Lock()
        self._cleanup_interval = timedelta(hours=1)
        self._last_cleanup = datetime.utcnow()

    def add_token(self, token: str) -> None:
        """
        Add a token to the blacklist

        Args:
            token: JWT token to blacklist
        """
        with self._lock:
            self._blacklist.add(token)
            self._auto_cleanup()

    def is_blacklisted(self, token: str) -> bool:
        """
        Check if a token is blacklisted

        Args:
            token: JWT token to check

        Returns:
            True if token is blacklisted, False otherwise
        """
        with self._lock:
            return token in self._blacklist

    def remove_token(self, token: str) -> bool:
        """
        Remove a token from the blacklist

        Args:
            token: JWT token to remove

        Returns:
            True if token was removed, False if not found
        """
        with self._lock:
            if token in self._blacklist:
                self._blacklist.remove(token)
                return True
            return False

    def clear(self) -> None:
        """Clear all tokens from the blacklist"""
        with self._lock:
            self._blacklist.clear()

    def size(self) -> int:
        """
        Get the number of blacklisted tokens

        Returns:
            Number of tokens in blacklist
        """
        with self._lock:
            return len(self._blacklist)

    def _auto_cleanup(self) -> None:
        """
        Automatically cleanup old entries periodically

        Note: This is a simple implementation. In production, implement
        proper expiration based on token exp claim.
        """
        now = datetime.utcnow()
        if now - self._last_cleanup > self._cleanup_interval:
            # In a real implementation, you would:
            # 1. Decode each token
            # 2. Check expiration time
            # 3. Remove expired tokens
            # For now, we just update the last cleanup time
            self._last_cleanup = now


# Global singleton instance
_token_blacklist_instance: TokenBlacklist = None


def get_token_blacklist() -> TokenBlacklist:
    """
    Get or create the global TokenBlacklist instance

    Returns:
        TokenBlacklist singleton instance
    """
    global _token_blacklist_instance
    if _token_blacklist_instance is None:
        _token_blacklist_instance = TokenBlacklist()
    return _token_blacklist_instance
