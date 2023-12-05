import unittest
from impl_part2 import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 35)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 1804)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample.txt"), 46)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 26829166)


if __name__ == '__main__':
    unittest.main()
