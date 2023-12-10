import unittest
from impl import process


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 4)

    def test_part1_sample2(self):
        self.assertEqual(process(1, "sample2.txt"), 8)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 6701)

    def test_part2_sample3(self):
        self.assertEqual(process(2, "sample3.txt"), 4)

    def test_part2_sample4(self):
        self.assertEqual(process(2, "sample4.txt"), 4)

    def test_part2_sample5(self):
        self.assertEqual(process(2, "sample5.txt"), 8)

    def test_part2_sample6(self):
        self.assertEqual(process(2, "sample6.txt"), 10)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 303)


if __name__ == '__main__':
    unittest.main()
