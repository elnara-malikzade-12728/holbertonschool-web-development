#!/usr/bin/env python3
"""basic_auth module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """A class inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """A function that returns the Base64 part if the
        Authorization header for a Basic Authentication
        """
        if (not isinstance(authorization_header, str) or
                authorization_header is None or
                not authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """A function that returns the decoded value of a Base64 string
        """
        if (not isinstance(base64_authorization_header, str) or
                base64_authorization_header is None):
            return None
        try:
            import base64
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """A function that returns the user email and
        password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return (None, None)
        parts = decoded_base64_authorization_header.split(':', 1)
        return (parts[0], parts[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """A function that returns the User instance
        based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        from models.user import User
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
