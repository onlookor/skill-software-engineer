import sys
import unittest

sys.path.insert(0, ".")
from calc import add


class ReproAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)


if __name__ == "__main__":
    unittest.main()

