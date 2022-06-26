#!/usr/bin/python3

""" Defines a class to manage database storage """

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from models.base_model import BaseModel, Base
from models.user import User
from models.game import Game


class DBStorage:
    """ manages database storage """
    __engine = None
    __session = None

    def __init__(self):
        """ constructor """
        user = environ.get('SENTEREZH_MYSQL_USER')
        pwd = environ.get('SENTEREZH_MYSQL_PWD')
        host = environ.get('SENTEREZH_MYSQL_HOST')
        db = environ.get('SENTEREZH_MYSQL_DB')
        env = environ.get('SENTEREZH_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      user, pwd, host, db), pool_pre_ping=True)
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
        if env == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ query database based on the class specified """
        session = self.__session
        dct = {}

        if not cls:
            classes = [User, State, City, Amenity, Place, Review]
        else:
            if type(cls) == str:
                cls = eval(csl)
            classes = [cls]

        for curr_class in classes:
            query = session.query(curr_class).all()
            for rows in query:
                key = "{}.{}".format(type(rows).__name__, rows.id)
                dct[key] = rows

        return dct

    def new(self, obj):
        """ add object to current session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit changes of the current session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete object on current session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
            creates all tables in the database and
            creates the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        ''' closes session '''
        self.__session.close()

    def get(self, cls, id):
        """ returns the object based on the class and id otherwise None """
        if cls not in classes.values():
            return None

        all = models.storage.all(cls)
        for val in all.values():
            if (val.id == id):
                return val

        return None

    def count(self, cls=None):
        """
            Returns the number of objects in storage matching the given class.
            If no class is passed, returns the count of all objects in storage.
        """
        all = classes.values()

        if not cls:
            count = 0
            for clas in all:
                count += len(models.storage.all(clas).values())
        else:
            count += len(models.storage.all(cls).values())

        return count
