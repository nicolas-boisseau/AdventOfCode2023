import unittest
from impl import process, custom_hash


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(1320, process(1, "sample.txt"),)

    def test_part1_input(self):
        self.assertEqual(522547, process(1, "input.txt"))

    def test_hash(self):
        print(custom_hash("rn"))

    def test_part2_sample(self):
        self.assertEqual(145, process(2, "sample.txt"))

    def test_part2_input(self):
        self.assertEqual(0, process(2, "input.txt"))


if __name__ == '__main__':
    unittest.main()
