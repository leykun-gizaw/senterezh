#!/usr/bin/python3

"""
    Defines a command line interface to handle objects
"""

import cmd
import sys

from models.base_model import BaseModel
from models import storage
from models.user import User
from models.game import Game


class SenterezhConsole(cmd.Cmd):
    """ Defines functionalities of the console """
    classes = {"BaseModel": BaseModel, "User": User, "Game": Game}
    prompt = "(senterezh) "
    file = None

    def precmd(self, line):
        """ initial configuration """
        if not sys.stdin.isatty:
            print()
        return line

    def do_quit(self, line):
        """Quit command to exit the program"""
        self.close()
        quit()

    def close(self):
        """ Finalize """
        if self.file:
            self.file.close()
            self.file = None

    def emptyline(self):
        """Do nothing if empty line specified"""
        pass

    def do_EOF(self, line):
        """Handle EOF"""
        print()
        return True

    def do_create(self, line):
        """Creates an object of any available class"""
        if not line:
            print("** class name missing **")
            return
        elif line not in SenterezhConsole.classes:
            print("** class doesn't exist **")
            return
        new_instance = SenterezhConsole.classes[line]()
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def test_arguments(self, line):
        """ test class existence, class name and instance id """
        new = line.partition(" ")
        class_name = new[0]
        class_id = new[2]
        success = 1

        if not class_name:
            print("** class name missing **")
            success = 0

        elif class_name not in SenterezhConsole.classes:
            print("** class doesn't exist **")
            success = 0

        elif not class_id:
            print("** instance id missing **")
            success = 0

        # guard aganist trailing whitespace
        if class_id and " " in class_id:
            class_id = class_id.partition(" ")[0]

        return (success, class_name, class_id)

    def do_show(self, line):
        """Shows string representation of an object instance"""
        result = self.test_arguments(line)

        if result[0]:
            class_key = result[1] + "." + result[2]
            try:
                print(storage._FileStorage__objects[class_key])
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all instances created or all instances of a certain class"""
        if line and line not in SenterezhConsole.classes:
            print("** class doesn't exist **")
            return

        lst = []
        for key, value in storage._FileStorage__objects.items():
            if line:
                if key.partition('.')[0] == line:
                    lst.append(str(storage._FileStorage__objects[key]))
            else:
                lst.append(str(storage._FileStorage__objects[key]))
        print(lst)

    def do_destroy(self, line):
        """Deletes an instance based on class name or id"""
        result = self.test_arguments(line)

        if result[0]:
            class_key = result[1] + "." + result[2]
            if class_key in storage._FileStorage__objects.keys():
                del storage._FileStorage__objects[class_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_update(self, line):
        """Updates an instance based on class name and id by
        adding or updating attribute"""
        result = self.test_arguments(line)
        if result[0]:
            tokens = line.split()
            if len(tokens) < 4:
                if len(tokens) == 2:
                    print("** attribute name missing **")
                    return
                elif len(tokens) == 3:
                    print("** value missing **")
                    return
            class_key = result[1] + "." + result[2]
            if class_key in storage._FileStorage__objects.keys():
                setattr(storage._FileStorage__objects[class_key],
                        tokens[2], tokens[3])
                storage.save()
            else:
                print("** no instance found **")

    def do_count(self, line):
        """Counts number of instances of a class"""
        if not line:
            print("** class name missing **")
            return
        if line not in SenterezhConsole.classes:
            print("** class doesn't exist **")
            return
        count = 0
        for key in storage._FileStorage__objects.keys():
            if key.split('.')[0] == line:
                count = count + 1
        print(count)


if __name__ == '__main__':
    SenterezhConsole().cmdloop()
