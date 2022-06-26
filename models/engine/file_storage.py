#!/usr/bin/python3

"""This module defines a class to manage file storage"""

import json
from os import path

from models.base_model import BaseModel
from models.user import User
from models.game import Game
   

classes = {'BaseModel': BaseModel, 'User': User, 'Game': Game}


class FileStorage:
    """This class manages storage of our models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """deletes the object obj from the attribute"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        ''' calls the reload method for deserialization '''
        self.reload()

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
