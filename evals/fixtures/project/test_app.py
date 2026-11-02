import unittest

from app import accepts


class AcceptanceTests(unittest.TestCase):
    def test_inside_limit(self):
        self.assertTrue(accepts(2, 3))

    def test_negative_rejected(self):
        self.assertFalse(accepts(-1, 3))


if __name__ == "__main__":
    unittest.main()
