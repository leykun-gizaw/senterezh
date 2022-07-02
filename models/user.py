#!/usr/bin/python3

"""
    Defines the User class
"""


from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, DateTime, Integer, String


class User(BaseModel, Base):
    """A blueprint for users (chess players)"""
    __tablename__ = "users"
    if storage_type == 'db':
        first_name = Column(String(20), nullable=False)
        last_name = Column(String(20), nullable=False)
        user_name = Column(String(20), nullable=False)
        birth_date = Column(DateTime, nullable=False)
        email = Column(String(30), nullable=False)
        password = Column(String(128), nullable=False)
        games_played = Column(Integer, default=0)
        score = Column(Integer, default=500)
        won = Column(Integer, default=0)
        draw = Column(Integer, default=0)
        lost = Column(Integer, default=0)
    else:
        first_name = ""
        last_name = ""
        user_name = ""
        games_played = 0
        total_score = 0
        won = 0
        lost = 0
        draw = 0
        email = ""
        password = ""
