#!/usr/bin/python3
import unittest
import tempfile
from datetime import datetime

from models import BaseModel, FileStorage


class TestBaseModelClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fp = tempfile.NamedTemporaryFile()
        cls.file_path = cls.fp.name
        cls.storage = FileStorage()
        cls.base = BaseModel()

    @classmethod
    def tearDownClass(cls):
        del cls.storage
        del cls.base
        cls.fp.close()

    def test_base_initialization(self):
        self.assertIsInstance(self.base.id, str)
        self.assertIsNotNone(self.base.created_at)
        self.assertIsInstance(self.base.created_at, datetime)
        self.assertIsNotNone(self.base.updated_at)
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_base_str(self):
        self.assertEqual(
            self.base.__str__(),
            f"[{self.base.__class__.__name__}] \
({self.base.id}) {self.base.__dict__}"
        )

    def test_base_save(self):
        prev_updated_at = self.base.updated_at
        self.base.save()

        self.assertNotEqual(self.base.updated_at, prev_updated_at)
        self.assertTrue(self.base.updated_at > prev_updated_at)

    def test_base_to_dict(self):
        bm_dict = self.base.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.base.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.base.updated_at.isoformat())

    def test_base_from_dict(self):
        bm_dict = self.base.to_dict()
        dummy_base_model = BaseModel(**bm_dict)
        self.assertEqual(bm_dict, dummy_base_model.to_dict())
