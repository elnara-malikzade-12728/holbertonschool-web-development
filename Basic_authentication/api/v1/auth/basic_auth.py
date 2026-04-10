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
