import unittest

from common.common import read_input_lines
from impl import part1, part2


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(46, part1(read_input_lines("sample.txt")))

    def test_part1_input(self):
        self.assertEqual(7543, part1(read_input_lines("input.txt")))

    def test_part2_sample(self):
        self.assertEqual(51, part2(read_input_lines("sample.txt")))

    def test_part2_input(self):
        self.assertEqual(8231, part2(read_input_lines("input.txt")))


if __name__ == '__main__':
    unittest.main()
