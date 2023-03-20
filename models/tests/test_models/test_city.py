#!/usr/bin/python3
import unittest
from datetime import datetime

from models import City, storage, BaseModel


class TestCityClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.city = City()

    def test_city_initialization(self):
        self.assertIsInstance(self.city.id, str)
        self.assertIsNotNone(self.city.created_at)
        self.assertIsInstance(self.city.created_at, datetime)
        self.assertIsNotNone(self.city.updated_at)
        self.assertIsInstance(self.city.updated_at, datetime)

        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

        self.assertIsInstance(self.city, BaseModel)
        self.assertEqual(type(self.city), City)

    def test_city_str(self):
        self.assertEqual(
            self.city.__str__(),
            f"[{self.city.__class__.__name__}] \
({self.city.id}) {self.city.__dict__}",
        )

    def test_city_save(self):
        prev_updated_at = self.city.updated_at
        self.city.save()

        self.assertNotEqual(self.city.updated_at, prev_updated_at)
        self.assertTrue(self.city.updated_at > prev_updated_at)

    def test_city_to_dict(self):
        bm_dict = self.city.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.city.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.city.updated_at.isoformat())

    def test_city_from_dict(self):
        bm_dict = self.city.to_dict()
        dummy_city = City(**bm_dict)
        self.assertEqual(bm_dict, dummy_city.to_dict())
