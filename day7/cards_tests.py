import unittest

from day7.cards import Card, Hand
from impl import process


class CardsTests(unittest.TestCase):

    def test_card_strength(self):
        self.assertEqual(Card('A').strength(), 14)

    def test_pair(self):
        self.assertEqual(Hand("AA123").is_pair(), True)
        self.assertEqual(Hand("AK123").is_pair(), False)

    def test_double_pair(self):
        self.assertTrue(Hand("AA8KK").is_double_pair())

    def test_three_of_a_kind(self):
        self.assertTrue(Hand("AAAK7").is_three_of_a_kind())

    def test_four_of_a_kind(self):
        self.assertTrue(Hand("AAAA7").is_four_of_a_kind())

    def test_full_house(self):
        self.assertTrue(Hand("AAAKK").is_full_house())

    def test_high_card(self):
        self.assertTrue(Hand("AKQJ9").is_high_card())
        self.assertFalse(Hand("AKKJ8").is_high_card())

    def test_compare(self):
        self.assertTrue(Hand("KTJJT") < Hand("KK677"))


if __name__ == '__main__':
    unittest.main()
