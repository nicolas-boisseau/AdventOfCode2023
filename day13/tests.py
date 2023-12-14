import unittest
from impl import process, read_patterns, cols_before, cols_after, rows_before, rows_after


class AdventOfCodeTests(unittest.TestCase):

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 405)

    def test_part1_sample2(self):
        self.assertEqual(405, process(1, "sample2.txt"))

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 30518)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample.txt"), 19)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 2508)

    def test_nico(self):
        with open("test.txt") as f:
            lines = [line.replace("\n", "") for line in f.readlines()]

            patterns = read_patterns(lines)
            middle = len(patterns[0]) // 2 + 1
            print(f"cols_before = {cols_before(patterns[0], middle)}")
            print(f"cols_after = {cols_after(patterns[0], middle)}")
            middle = len(patterns[0]) // 2 + 1
            print(f"rows_before = {rows_before(patterns[0], middle)}")
            print(f"rows_after = {rows_after(patterns[0], middle)}")

    def test_nico(self):
        with open("test.txt") as f:
            lines = [line.replace("\n", "") for line in f.readlines()]

            reductor=2
            patterns = read_patterns(lines)
            middle = len(patterns[0]) // 2 + 1
            print(f"cols_before = {cols_before(patterns[0], middle, reductor)}")
            print(f"cols_after = {cols_after(patterns[0], middle, reductor)}")
            middle = len(patterns[0]) // 2 + 1
            print(f"rows_before = {rows_before(patterns[0], middle, reductor)}")
            print(f"rows_after = {rows_after(patterns[0], middle, reductor)}")

if __name__ == '__main__':
    unittest.main()
