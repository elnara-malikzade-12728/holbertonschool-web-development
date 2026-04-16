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
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str):
        """Takes a single session_id string argument and
        returns the corresponding User or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Takes a single user_id integer argument and returns None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Takes an email string argument and returns a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
