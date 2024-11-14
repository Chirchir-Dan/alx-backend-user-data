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
        Determines if a given path requires authentication.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): A list of paths that do not
            require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else f"{path}/"

        for excluded_path in excluded_paths:
            # Handle wildcards at the end of excluded paths
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
                elif normalized_path == excluded_path:
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
