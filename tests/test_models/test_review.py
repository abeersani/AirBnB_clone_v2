#!/usr/bin/python3
import unittest
from datetime import datetime

from models import Review, storage, BaseModel


class TestReviewClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = Review()

    def test_review_initialization(self):
        self.assertIsInstance(self.review.id, str)
        self.assertIsNotNone(self.review.created_at)
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsNotNone(self.review.updated_at)
        self.assertIsInstance(self.review.updated_at, datetime)

        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

        self.assertIsInstance(self.review, BaseModel)
        self.assertEqual(type(self.review), Review)

    def test_review_str(self):
        self.assertEqual(
            self.review.__str__(),
            f"[{self.review.__class__.__name__}] \
({self.review.id}) {self.review.__dict__}",
        )

    def test_review_save(self):
        prev_updated_at = self.review.updated_at
        self.review.save()

        self.assertNotEqual(self.review.updated_at, prev_updated_at)
        self.assertTrue(self.review.updated_at > prev_updated_at)

    def test_review_to_dict(self):
        bm_dict = self.review.to_dict()

        self.assertIsInstance(bm_dict, dict)
        self.assertTrue(all([isinstance(v, str) for k, v in bm_dict.items()]))
        self.assertEqual(
                bm_dict["created_at"], self.review.created_at.isoformat())
        self.assertEqual(
                bm_dict["updated_at"], self.review.updated_at.isoformat())

    def test_review_from_dict(self):
        bm_dict = self.review.to_dict()
        dummy_review = Review(**bm_dict)
        self.assertEqual(bm_dict, dummy_review.to_dict())


# if __name__ == "__main__":
# Do stuff
