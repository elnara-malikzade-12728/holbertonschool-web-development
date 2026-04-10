#!/usr/bin/env python3
"""basic_auth module
"""
from api.v1.auth.auth import Auth


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
