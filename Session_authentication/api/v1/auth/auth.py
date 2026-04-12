#!/usr/bin/env python3
"""Auth module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Class for authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function for choosing the right paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        normalized_path = path if path.endswith('/') else path + '/'
        if normalized_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """A function for authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """A function for user
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')

        return request.cookies.get(session_name)
