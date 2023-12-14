import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(0, process(1, "sample.txt"),)

    def test_part1_input(self):
        self.assertEqual(0, process(1, "input.txt"))

    def test_part2_sample(self):
        self.assertEqual(0, process(2, "sample.txt"))

    def test_part2_input(self):
        self.assertEqual(0, process(2, "input.txt"))


if __name__ == '__main__':
    unittest.main()
