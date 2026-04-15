#!/usr/bin/env python3
"""A module for authentication
"""
import uuid
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


def _generate_uuid() -> str:
    """Function returns a string representation of a new uuid
    """
    return str(uuid.uuid4())


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
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8')):
                return True
        except (NoResultFound, AttributeError):
            return False
        return False

    def create_session(self, email: str) -> str:
        """The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the
        user's session_id, then return the session ID.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise NoResultFound
        else:
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
