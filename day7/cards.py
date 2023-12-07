from py_linq import Enumerable

card_strengths = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

class Card:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return self.label

    def strength(self):
        return card_strengths[self.label]

    def __lt__(self, other):
        return self.strength() < other.strength()
class Hand:
    def __init__(self, cards, bid=0):
        self.cards = [Card(card) for card in cards]
        self.bid = bid

    def to_string(self):
        res = ""
        for card in self.cards:
            res += card.label
        return res

    def is_pair(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).any(lambda group: len(group) == 2)

    def is_double_pair(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).count(lambda group: len(group) == 2) == 2

    def is_three_of_a_kind(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).any(lambda group: len(group) == 3)

    def is_five_of_a_kind(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).any(lambda group: len(group) == 5)

    def is_four_of_a_kind(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).any(lambda group: len(group) == 4)

    def is_full_house(self):
        return self.is_pair() and self.is_three_of_a_kind()

    def is_high_card(self):
        return Enumerable(self.cards).group_by(key=lambda card: card.label).count(lambda group: len(group) == 1) == 5

    def kind(self):
        if self.is_five_of_a_kind():
            return "five_of_a_kind", 7
        elif self.is_four_of_a_kind():
            return "four_of_a_kind", 6
        elif self.is_full_house():
            return "full_house", 5
        elif self.is_three_of_a_kind():
            return "three_of_a_kind", 4
        elif self.is_double_pair():
            return "double_pair", 3
        elif self.is_pair():
            return "pair", 2
        elif self.is_high_card():
            return "high_card", 1
        return "nawak", -1

    def lt_compare_hands(self, other):
        for i, card in enumerate(self.cards):
            if self.cards[i].strength() == other.cards[i].strength():
                continue
            elif self.cards[i].strength() < other.cards[i].strength():
                return True
            else:
                return False
        return False

    def __lt__(self, other):
        selfKind, selfStrength = self.kind()
        otherKind, otherStrength = other.kind()
        print(f"{selfKind}={selfStrength} VS {otherKind}={otherStrength}")
        if selfKind == otherKind and selfKind != "nawak" and otherKind != "nawak":
            res = self.lt_compare_hands(other)
            print(f"{res}")
            return res
        else:
            if selfStrength != -1 and otherStrength == -1:
                print("False")
                return False
            elif selfStrength == -1 and otherStrength != -1:
                print("True")
                return True
            elif selfStrength < otherStrength :
                print("True")
                return True
            else:
                print("False")
                return False

        return False

class Game:
    def __init__(self):
        self.hands = []

    def __str__(self):
        return str(self.hands)

    def add_hand(self, hand):
        self.hands.append(hand)

    def total_score(self):
        self.hands.sort()

        score = 0
        for i in range(len(self.hands)-1, -1, -1):
            hand = self.hands[i].to_string()
            hand_score = self.hands[i].bid * (i + 1)
            #print(f"{hand} : bid={self.hands[i].bid} and score= {hand_score}")
            score += self.hands[i].bid * (i + 1)
        return score