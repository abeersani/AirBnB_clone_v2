#!/usr/bin/python3
"""
This module defines the entry point of the hbnb command interpreter used
to interact with hbnb framework
"""
import cmd
import json
import shlex
import textwrap
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def strip(s):
    return s.strip("'").strip('"')


class HBNBCommand(cmd.Cmd):
    """Simple command processor for the hbnb project"""

    prompt = "(hbnb) "
    hbnb_classes = ["BaseModel", "User", "State",
                    "City", "Amenity", "Place", "Review"]

    def do_EOF(self, arg):
        """Exit"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def postloop(self):
        print()

    def emptyline(self):
        """Action if empty line (don't do anything)"""
        pass

    def precmd(self, arg):
        """Capture help commands and parse method docstring using textwrap"""

        command, args, line = cmd.Cmd.parseline(self, arg)
        if command == "help" and args != "":
            eval_str = line.replace("help", "do").replace(" ", "_")
            eval_str = f"self.{eval_str}.__doc__"
            try:
                ret = textwrap.dedent(eval(eval_str)).lstrip("\n")
                print(ret)
            except AttributeError:
                print("No such command")
            finally:
                return ""

        return line

    def do_create(self, arg):
        """
        Create new instance of Class, save to json file and print id
            Ex:
            >> create BaseModel
            >> Create User
        """
        if not arg:
            print("** class name missing **")

        elif arg not in self.hbnb_classes:
            print("** class doesn't exist **")

        else:
            eval_string = f"{arg}()"
            new_base = eval(eval_string)
            new_base.save()
            print(new_base.id)

    def do_show(self, arg):
        """
        Print string representation of instance if it exists
            Ex:
            >> show Basemodel <id>
            >> BaseModel.show(<id>)
        """
        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing **")

                else:
                    storage.reload()
                    instance_key = f"{argv[0]}.{strip(argv[1])}"
                    instance = storage.all().get(instance_key, None)

                    if instance is None:
                        print("** no instance found **")
                    else:
                        print(instance)

    def do_destroy(self, arg):
        """
        Delete instance base on class name and id, save to json file
            Ex:
            >> destroy BaseModel <id>
            >> BaseModel.destroy(<id>)
        """
        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing **")

                else:
                    storage.reload()
                    instance_key = f"{argv[0]}.{strip(argv[1])}"
                    instance = storage.all().get(instance_key, None)

                    if instance is None:
                        print("** no instance found **")
                    else:
                        storage.all().pop(instance_key)
                        storage.save()

    def do_all(self, arg):
        """
        Print string representation of all instances
            Ex:
            >> all BaseModel
            >> BaseModel.all()
        """

        def eval_str(string):
            return string.split(".")[0]

        storage.reload()

        if arg == "":
            print(json.dumps([str(v) for k, v in storage.all().items()]))

        else:
            if arg not in self.hbnb_classes:
                print("** class doesn't exist **")
            else:
                print(
                    json.dumps(
                        [
                            str(v)
                            for k, v in storage.all().items()
                            if arg == v.__class__.__name__
                        ]
                    )
                )

    def do_update(self, arg):
        """
        Update/Add instance attribute based on class, name and id
            Ex:
            >> update BaseModel <id> <attr> <attr_value>
            >> BaseModel.update(<id> <attr> <attr_value>
            >> BaseModel.update(<id> {"first_name": "BaseModel1", "Age": 10})
        """

        if not arg:
            print("** class name missing **")

        else:
            # argv = shlex.split(arg)
            argv = arg.split()
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")
                return

            if argc < 2:
                print("** instance id missing **")
                return

            else:
                storage.reload()
                instance_key = f"{argv[0]}.{strip(argv[1])}"
                instance = storage.all().get(instance_key, None)

                if instance is None:
                    print("** no instance found **")
                else:
                    if argc < 3:
                        print("** attribute name missing **")
                        return
                    try:
                        if argv[2].startswith("{") and argv[2].endswith("}"):
                            instance.__dict__.update(json.loads(argv[2]))
                            storage.save()
                            return
                    except (ValueError, json.decoder.JSONDecodeError):
                        pass

                    if argc < 4:
                        print("** value missing **")
                        return
                    else:
                        dont_update = ["id", "created_at", "updated_at"]
                        attribute = strip(argv[2])
                        if attribute not in dont_update:
                            instance.__dict__[strip(argv[2])] = strip(argv[3])
                            storage.save()

    def do_count(self, arg):
        """
        Count number of instances of a class
            Ex:
            >> count BaseModel
            >> BaseModel.count()
        """

        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")
            else:
                storage.reload()
                count = [v for v in storage.all().values()
                         if arg == v.__class__.__name__
                         ]
                print(len(count))

    def default(self, arg):
        """Parse unrecognized command prefixes"""

        # parseline returns tuple (command, args, line)
        command, args, line = cmd.Cmd.parseline(self, arg)
        # ex. arg = User.all()
        # command, args, line = ("User", ".all()",  "User.all()")

        # if command in self.hbnb_classes:
        do_cmd, _, add_args = args.strip(".)").partition("(")

        if do_cmd == "":
            print("No command found, use help")
            return

        if add_args == "":
            new_arg = f"{do_cmd} {command}"

        else:
            # Convert args to a list and join with spaces
            add_args = add_args.split(",", 1)
            for idx, add_arg in enumerate(add_args):
                if add_arg.strip().startswith("{"):
                    add_args[idx] = add_arg.replace(
                            " ", "").replace("'", '"')
                else:
                    add_args[idx] = add_arg.replace(",", "")

            add_args = " ".join(add_args)
            new_arg = f"{do_cmd} {command} {add_args}"

        cmd.Cmd.onecmd(self, new_arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
