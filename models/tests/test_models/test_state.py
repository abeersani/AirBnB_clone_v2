#!/usr/bin/python3

import unittest
from datetime import datetime

from models import State, storage, BaseModel


class TestStateClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State()

    def test_state_initialization(self):
        self.assertIsInstance(self.state.id, str)
        self.assertIsNotNone(self.state.created_at)
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsNotNone(self.state.updated_at)
        self.assertIsInstance(self.state.updated_at, datetime)

        self.assertEqual(self.state.name, "")

        self.assertIsInstance(self.state, BaseModel)
        self.assertEqual(type(self.state), State)

    def test_state_str(self):
        self.assertEqual(
            self.state.__str__(),
            f"[{self.state.__class__.__name__}] \
({self.state.id}) {self.state.__dict__}",
        )

    def test_state_save(self):
        prev_updated_at = self.state.updated_at
        self.state.save()

        self.assertNotEqual(self.state.updated_at, prev_updated_at)
        self.assertTrue(self.state.updated_at > prev_updated_at)

    def test_state_to_dict(self):
        bm_dict = self.state.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.state.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.state.updated_at.isoformat())

    def test_state_from_dict(self):
        bm_dict = self.state.to_dict()
        dummy_state = State(**bm_dict)
        self.assertEqual(bm_dict, dummy_state.to_dict())
