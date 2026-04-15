#!/usr/bin/env python3
"""A module for authentication
"""
import bcrypt
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hashes a password string using bcrypt and returns a string
    """
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """takes mandatory email and password string arguments
        and returns a User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists". format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)

        return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Takes the arguments and returns a boolean
        """
        user = self._db.find_user_by(email=email)
        if user and bcrypt.checkpw(password.encode('utf-8'), 
                               user.hashed_password.encode('utf-8')):
            return True
        return False
