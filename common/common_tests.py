import unittest
from common import Capture, PostAnswer


class CommonTests(unittest.TestCase):

    def test_Capture_One(self):
        # arrange
        inputPattern = r"blabla (\d+) blabla"
        input = "blabla 123 blabla"

        # act
        result = Capture(inputPattern, input)

        self.assertEqual(result[0], "123")

    def test_Capture_Three(self):
        # arrange
        inputPattern = r"(\d+),(\d+) -> (\d+),(\d+)"
        input = "4,6 -> 12,24"

        # act
        result = Capture(inputPattern, input)

        self.assertEqual(result[0], "4")
        self.assertEqual(result[1], "6")
        self.assertEqual(result[2], "12")
        self.assertEqual(result[3], "24")

    def test_PostAnswer(self):
        # arrange
        url = "https://adventofcode.com/2022/day/1/answer"

        # act
        result = PostAnswer(url, "67016")

