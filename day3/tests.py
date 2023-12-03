import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 4361)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 517021)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample.txt"), 467835)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 81296995)


if __name__ == '__main__':
    unittest.main()
