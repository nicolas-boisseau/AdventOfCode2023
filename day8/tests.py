import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 2)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 15989)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample2.txt"), 6)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 13830919117339)


if __name__ == '__main__':
    unittest.main()
