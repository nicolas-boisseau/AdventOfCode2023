import unittest

from py_linq import Enumerable


class PyLinqTests(unittest.TestCase):

    def test_enumerable(self):
        self.assertEqual(Enumerable([1, 2, 3]).to_list(), [1, 2, 3])

    def test_groupby(self):
        self.assertAlmostEqual(
            Enumerable(["a", "b", "a", "c"]).distinct().to_list(),
            ["a", "b", "c"])

    def test_agg(self):
        self.assertEqual(
            Enumerable([1, 2, 3]).aggregate(0, lambda acc, x: acc + x),
            6)

    def test_agg_str(self):
        self.assertEqual(
            Enumerable(["a", "b", "c"]).aggregate(lambda acc, x: acc + x),
            "abc")
