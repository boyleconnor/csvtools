import unittest
from column_functions import COUNT, SUM, MIN, MAX, FIRST, LAST


class TestCount(unittest.TestCase):

    def test_count(self):
        self.assertEqual(COUNT([1, 'h', 123, '87']), 4)

    def test_empty_count(self):
        self.assertEqual(COUNT([]), 0)


class TestSum(unittest.TestCase):

    def test_int_sum(self):
        self.assertEqual(SUM(['1', '2', '100']), 103)

    def test_float_sum(self):
        self.assertEqual(SUM(['100.1', '2.5', '1.0']), 103.6)

    def test_mixed_sum(self):
        self.assertEqual(SUM(['100', '2.5', '1.0']), 103.5)

    def test_bad_sum(self):
        with self.assertRaises(ValueError):
            SUM(['1', '1.0', 'a'])


class TestMinMax(unittest.TestCase):

    def test_int_min(self):
        self.assertEqual(MIN(['1123', '2', '10']), 2)
        self.assertEqual(MIN(['-1123', '2', '-10']), -1123)

    def test_float_min(self):
        self.assertEqual(MIN(['1123.0', '2.0', '10.1']), 2.0)
        self.assertEqual(MIN(['-1123.3', '2.0', '-10.0']), -1123.3)

    def test_bad_min(self):
        with self.assertRaises(ValueError):
            MIN(['1', '1.0', 'a'])

    def test_int_max(self):
        self.assertEqual(MAX(['1123', '2', '10']), 1123)
        self.assertEqual(MAX(['-1123', '-2', '-10']), -2)

    def test_float_max(self):
        self.assertEqual(MAX(['1123.3', '2.1', '10.3']), 1123.3)
        self.assertEqual(MAX(['-1123.1', '-2.4', '-10.6']), -2.4)

    def test_bad_max(self):
        with self.assertRaises(ValueError):
            MAX(['1', '1.0', 'a'])
