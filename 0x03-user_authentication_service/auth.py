#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth class with a database instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password with a random salt using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))
