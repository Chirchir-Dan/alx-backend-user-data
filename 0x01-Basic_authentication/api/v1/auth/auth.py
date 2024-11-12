#!/usr/bin/env python3
"""
Authentication module
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Template class for API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path
        Args:
            path (str): The path to check
            excluded_paths (List[str]): List of paths that don't
            require authentication
        Returns:
            bool: False for now, logic will be added later
        """
        if path is None or not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else f"{path}/"

        if normalized_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the Flask request
        Args:
            request: Flask request object
        Returns:
            str: None for now, logic will be added later
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        Args:
            request: Flask request object
        Returns:
            TypeVar('User'): None for now, logic will be added later
        """
        return None
