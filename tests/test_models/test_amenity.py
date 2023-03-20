#!/usr/bin/python3
import unittest
from datetime import datetime

from models import Amenity, storage, BaseModel


class TestAmenityClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amenity = Amenity()

    def test_amenity_initialization(self):
        self.assertIsInstance(self.amenity.id, str)
        self.assertIsNotNone(self.amenity.created_at)
        self.assertIsInstance(self.amenity.created_at, datetime)
        self.assertIsNotNone(self.amenity.updated_at)
        self.assertIsInstance(self.amenity.updated_at, datetime)

        self.assertEqual(self.amenity.name, "")

        self.assertIsInstance(self.amenity, BaseModel)
        self.assertEqual(type(self.amenity), Amenity)

    def test_amenity_str(self):
        self.assertEqual(
            self.amenity.__str__(),
            f"[{self.amenity.__class__.__name__}] \
({self.amenity.id}) {self.amenity.__dict__}",
        )

    def test_amenity_save(self):
        prev_updated_at = self.amenity.updated_at
        self.amenity.save()

        self.assertNotEqual(self.amenity.updated_at, prev_updated_at)
        self.assertTrue(self.amenity.updated_at > prev_updated_at)

    def test_amenity_to_dict(self):
        bm_dict = self.amenity.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.amenity.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.amenity.updated_at.isoformat())

    def test_amenity_from_dict(self):
        bm_dict = self.amenity.to_dict()
        dummy_amenity = Amenity(**bm_dict)
        self.assertEqual(bm_dict, dummy_amenity.to_dict())
