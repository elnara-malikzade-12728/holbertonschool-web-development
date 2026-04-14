#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import User, Base
from bcrypt import hashpw

class DB:
    """Database class
    """

    def __init__(self):
        """Database initialization
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Session Function, returns session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Returns a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Takes arbitrary keyword arguments and returns the first row
        found in the users table, or None if no user is found.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Takes as argument a required user_id integer and arbitrary
        keyword arguments, and returns None
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
