#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import User, Base


class DB:

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

    def find_user_by(self, **kwargs):
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
