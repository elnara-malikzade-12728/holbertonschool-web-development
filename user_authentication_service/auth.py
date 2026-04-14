#!/usr/bin/env python3
"""A module for authentication
"""


def _hash_password(self, password: str) -> str:
    """A function to hash the given password and return a string                                                          
    """
    hashed_bytes = hashpw(password.encode('utf-8'), gensalt())
    return hashed_bytes.decode('utf-8')
