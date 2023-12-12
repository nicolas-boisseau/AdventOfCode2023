import unittest
from impl import process, is_match_record, get_mutations_for


class AdventOfCodeTests(unittest.TestCase):

    def test_is_match_record(self):
        self.assertTrue(is_match_record("#.#.###", [1,1,3]))

    def test_get_mutations_for(self):
        print(list(get_mutations_for(3)))
        self.assertEqual(8, len(list(get_mutations_for(3))))

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 21)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 7718)

    def test_part2_sample(self):
        self.assertEqual(process(2, "sample.txt"), 19)

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 2508)


if __name__ == '__main__':
    unittest.main()
