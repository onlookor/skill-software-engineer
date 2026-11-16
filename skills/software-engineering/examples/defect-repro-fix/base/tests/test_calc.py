import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from calc import mul


class TestCalc(unittest.TestCase):
    def test_mul(self):
        self.assertEqual(mul(2, 3), 6)
