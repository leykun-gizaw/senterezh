#!/usr/bin/python3

"""
    Defines the Game class
"""

from models.base_model import BaseModel, Base
from models import storage_type
from models.user import User

from sqlalchemy import Column, ForeignKey, Integer, String, Text


class Game(BaseModel, Base):
    """A blueprint for a game"""
    __tablename__ = "game"
    if storage_type == 'db':
        player_1_id = Column(
                        String(60),
                        ForeignKey('users.id'),
                        nullable=False)
        player_2_id = Column(
                        String(60),
                        ForeignKey('users.id'),
                        nullable=False)
        type = Column(String(20), nullable=False)
        duration = Column(Integer, nullable=False)
        moves = Column(Text, nullable=False)
    else:
        player_1_id = ""
        player_2_id = ""
        type = ""
        duration = ""
        moves = ""
