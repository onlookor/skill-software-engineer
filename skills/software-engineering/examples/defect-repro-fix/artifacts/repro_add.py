import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from calc import add


class ReproAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
