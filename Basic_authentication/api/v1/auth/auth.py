#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar

class Auth():
    """Class for authentication
    """


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function for choosing the right paths
        """
        return False


    def authorization_header(self, request=None) -> str:
        """A function for authorization header
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """A function for user
        """
        return None
        
