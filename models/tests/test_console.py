#!/usr/bin/python3

import unittest
import json
from io import StringIO
from unittest import mock
from console import HBNBCommand


class TestCMD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actions = [
            action.partition("_")[2]
            for action in dir(HBNBCommand())
            if action.startswith("do_")
        ]
        cls.classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review",
        ]

    def setUp(self):
        self.cmd = HBNBCommand()

    def teardown(self):
        self.cmd.onecmd("quit")

    def test_quit(self):
        self.assertEqual(
            self.cmd.do_quit.__doc__, "Quit command to exit the program"
        )

    def test_EOF(self):
        self.assertEqual(self.cmd.do_EOF.__doc__, "Exit")

    def test_emptyline(self):
        self.assertEqual(
            self.cmd.emptyline.__doc__,
            "Action if empty line (don't do anything)",
        )

    def test_print_help(self):
        for action in self.actions:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"help {action}")
                self.assertEqual(
                    f.getvalue().strip(),
                    eval(f"self.cmd.do_{action}.__doc__.strip()"),
                )

    def test_prompt(self):
        self.assertEqual(self.cmd.prompt, "(hbnb) ")

    def test_class_name_missing(self):
        for action in ["create", "show", "update", "destroy", "count"]:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{action}")
                self.assertEqual(
                    f.getvalue().strip(), "** class name missing **"
                )

    def test_class_doest_exist(self):
        for action in ["create", "show", "update", "destroy", "count"]:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{action} MyModel")
                self.assertEqual(
                    f.getvalue().strip(), "** class doesn't exist **"
                )

    def test_class_id_missing(self):
        for action in ["show", "update", "destroy"]:
            for klass in self.classes:
                with mock.patch("sys.stdout", new=StringIO()) as f:
                    self.cmd.onecmd(f"{action} {klass}")
                    self.assertEqual(
                        f.getvalue().strip(), "** instance id missing **"
                    )

    def test_all(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
                self.assertIn(f"[{klass}]", f.getvalue().strip())
                self.assertNotIn(
                    f"[{self.classes[idx-1]}]", f.getvalue().strip()
                )

    def test_class_all(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{klass}.all()")
                self.assertIn(f"[{klass}]", f.getvalue().strip())
                self.assertNotIn(
                    f"[{self.classes[idx-1]}]", f.getvalue().strip()
                )

    def test_count(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"count {klass}")
                self.assertIsInstance(int(f.getvalue()), int)

    def test_class_count(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{klass}.count()")
                self.assertIsInstance(int(f.getvalue()), int)

    def test_show(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")
            # print(f.getvalue())
                self.assertIn(f"{obj_id}", f.getvalue())

    def test_class_show(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            # class_list = json.loads(f.getvalue())
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{klass}.show({obj_id})")
            # print(f.getvalue())
                self.assertIn(f"{obj_id}", f.getvalue())

    def test_update(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            # class_list = json.loads(f.getvalue())
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            c = f'update {klass} {obj_id} "attribute_name", "string_value"'
            self.cmd.onecmd(c)

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")

                self.assertIn("attribute_name", f.getvalue())

    def test_class_update(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            # class_list = json.loads(f.getvalue())
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            c = f'{klass}.update({obj_id} "attribute_name", "string_value")'
            self.cmd.onecmd(c)

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")

                self.assertIn("attribute_name", f.getvalue())

    def test_update_dict(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            # class_list = json.loads(f.getvalue())
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            c = f'update {klass} {obj_id} {{"attribute_name": "string_value"}}'
            self.cmd.onecmd(c)

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")

                self.assertIn("attribute_name", f.getvalue())

    def test_class_update_dict(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            # class_list = json.loads(f.getvalue())
            obj_string = f.getvalue()
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            c = f'{klass}.update({obj_id} {{"attribute_name":"string_value"}})'
            self.cmd.onecmd(c)

            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")

                self.assertIn("attribute_name", f.getvalue())

    def test_destroy(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            class_list = json.loads(f.getvalue())
            obj_string = class_list[0]
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            self.cmd.onecmd(f"destroy {klass} {obj_id}")
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")
                self.assertEqual(
                        f.getvalue().strip(), '** no instance found **')

    def test_class_destroy(self):
        for idx, klass in enumerate(self.classes):
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"all {klass}")
            class_list = json.loads(f.getvalue())
            obj_string = class_list[0]
            start, end = obj_string.find("("), obj_string.find(")")
            obj_id = obj_string[start+1:end]

            self.cmd.onecmd(f"{klass}.destroy({obj_id})")
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"show {klass} {obj_id}")
                self.assertEqual(
                        f.getvalue().strip(), '** no instance found **')
