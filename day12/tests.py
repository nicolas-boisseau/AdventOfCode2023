import unittest
from impl import process, is_match_record, get_mutations_for, multiply_sequence, find_mutations, compute_possibilities


class AdventOfCodeTests(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(".#?.#?.#?.#?.#", multiply_sequence(".#", "?", 5))

    def test_is_match_record(self):
        self.assertTrue(is_match_record("#.#.###", [1,1,3]))

    def test_get_mutations_for(self):
        print(list(get_mutations_for(3)))
        self.assertEqual(8, len(list(get_mutations_for(3))))

    def test_part1_sample(self):
        self.assertEqual(process(1, "sample.txt"), 21)

    def test_part1_input(self):
        self.assertEqual(process(1, "input.txt"), 7718)

    def test_part2_mutations(self):
        spring_row = multiply_sequence("???.###", "?", 5)
        records = [int(d) for d in multiply_sequence("1,1,3", ",", 5).split(",")]
        self.assertEqual(1, len(find_mutations(spring_row, records)))

    def test_compute_possibilities(self):
        records = [1,1,3]
        self.assertEqual(4, len(compute_possibilities(records, len(".??..??...?##."))))

    def test_part2_sample(self):
        self.assertEqual(1, process(2, "sample.txt"))

    def test_part2_input(self):
        self.assertEqual(process(2, "input.txt"), 2508)


if __name__ == '__main__':
    unittest.main()
