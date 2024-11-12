#!/usr/bin/env python3
"""
BasicAuth module for basic authentication.
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 encoded part of the header if valid,
            otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # Extract and return the Base64 part after "Basic "
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string and convert to UTF-8
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            # Handle invalid Base64 or non-UTF-8 content
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the decoded Base64 value.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64 string.

        Returns:
            tuple: A tuple containing the user email and password,
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string at the first ':' and return the email and password
        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on user email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The corresponding User instance if valid credentials
            are provided.
            None: If any validation fails (invalid email, password,
            or user not found).
        """
        # Validate email and password types
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        if user_email is None or user_pwd is None:
            return None

        # Lookup user by email
        user = User.search({"email": user_email})
        if not user:
            return None  # No user found with this email

        # Check if password matches
        if not user[0].is_valid_password(user_pwd):
            return None  # Password does not match

        # Return the user instance if email and password are valid
        return user[0]
