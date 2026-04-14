#!/usr/bin/env python3
"""A module for authentication
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hashes a password string using bcrypt and returns a string
    """
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')
