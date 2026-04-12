#!/usr/bin/env python3
"""session_auth module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth inherits from Auth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """A function to create a Session ID for the user_id
        """
        if (not isinstance(user_id, str) or
                user_id is None):
            return None
        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
