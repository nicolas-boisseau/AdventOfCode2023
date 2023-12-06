import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 288)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 449820)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample.txt"), 71503)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 42250895)


if __name__ == '__main__':
    unittest.main()
