import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(374, process(1, "sample.txt"))

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 9177603)

    def test_part2_sample(self):
        self.assertEqual(1030, process(2, "sample.txt", 10))
        self.assertEqual(8410, process(2, "sample.txt", 100))

    def test_part2_input(self):
        self.assertEqual(632003913611, process(2, "input.txt", 1000000))


if __name__ == '__main__':
    unittest.main()
