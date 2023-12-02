import unittest
from common import capture, post_answer


class CommonTests(unittest.TestCase):

    def test_Capture_One(self):
        # arrange
        input_pattern = r"blabla (\d+) blabla"
        input_data = "blabla 123 blabla"

        # act
        result = capture(input_pattern, input_data)

        self.assertEqual(result[0], "123")

    def test_Capture_Three(self):
        # arrange
        input_pattern = r"(\d+),(\d+) -> (\d+),(\d+)"
        input_data = "4,6 -> 12,24"

        # act
        result = capture(input_pattern, input_data)

        self.assertEqual(result[0], "4")
        self.assertEqual(result[1], "6")
        self.assertEqual(result[2], "12")
        self.assertEqual(result[3], "24")

    @staticmethod
    def test_post_answer():
        # arrange
        url = "https://adventofcode.com/2022/day/16/answer"

        # act
        post_answer(url, 1, "67016")
