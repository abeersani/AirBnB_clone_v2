#!/usr/bin/python3
import unittest
from datetime import datetime

from models import User, storage, BaseModel


class TestUserClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User()

    def test_user_initialization(self):
        self.assertIsInstance(self.user.id, str)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsInstance(self.user.updated_at, datetime)

        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

        self.assertIsInstance(self.user, BaseModel)
        self.assertEqual(type(self.user), User)

    def test_user_str(self):
        self.assertEqual(
            self.user.__str__(),
            f"[{self.user.__class__.__name__}] \
({self.user.id}) {self.user.__dict__}",
        )

    def test_user_save(self):
        prev_updated_at = self.user.updated_at
        self.user.save()

        self.assertNotEqual(self.user.updated_at, prev_updated_at)
        self.assertTrue(self.user.updated_at > prev_updated_at)

    def test_user_to_dict(self):
        bm_dict = self.user.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.user.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.user.updated_at.isoformat())

    def test_user_from_dict(self):
        bm_dict = self.user.to_dict()
        dummy_user = User(**bm_dict)
        self.assertEqual(bm_dict, dummy_user.to_dict())


# if __name__ == "__main__":
# Do stuff
