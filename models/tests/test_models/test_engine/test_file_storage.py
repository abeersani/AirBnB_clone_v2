#!/usr/bin/python3
import unittest
import tempfile
from models import BaseModel, FileStorage


class TestFileStorage(unittest.TestCase):

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

    def test_new(self):
        self.storage.new(self.base)
        self.assertIn(self.base,
                      [v for k, v in self.storage.all().items()])

    def test_all(self):
        self.assertIsInstance(self.storage.all(), dict)
        self.assertTrue(
                all([isinstance(v, BaseModel)
                     for k, v in self.storage.all().items()])
                )

    def test_save(self):
        self.storage.new(self.base)
        self.storage.save()
        self.storage.reload()
        self.assertIn(self.base,
                      [v for k, v in self.storage.all().items()])

    def test_reload(self):
        for i in range(5):
            self.storage.new(BaseModel())

        self.storage.new(self.base)
        self.storage.save()
        self.storage.reload()

        self.assertTrue(self.storage.all() != {})
        self.assertIn(self.base,
                      [v for k, v in self.storage.all().items()])
