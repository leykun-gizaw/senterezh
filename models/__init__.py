#!/usr/bin/python3

"""
    Instantiates a storage
"""

from os import getenv


storage_type = getenv('SENTEREZH_STORAGE_TYPE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
