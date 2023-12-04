import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


class ScratchCard:

    def str(self):
        return f"Card {self.id} : {self.win_numbers} | {self.played_numbers}"

    def __init__(self, id, win_numbers, played_numbers):
        self.id = id
        self.win_numbers = win_numbers
        self.played_numbers = played_numbers

    def get_score(self):
        current_score = 0
        nb_won_numbers = 0
        for played_number in self.played_numbers:
            if played_number in self.win_numbers:
                nb_won_numbers += 1
                if current_score == 0:
                    current_score = 1
                else:
                    current_score *= 2

        return current_score, nb_won_numbers


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        cards = []
        for line in lines:
            splitted = line.split(": ")
            card_id = int(capture(r"Card[ ]+(\d+)", splitted[0])[0])
            game = splitted[1].split(" | ")
            win_numbers = capture_all(r"(\d+)", game[0])
            played_numbers = capture_all(r"(\d+)", game[1])
            win_numbers = [int(number) for number in win_numbers]
            played_numbers = [int(number) for number in played_numbers]

            cards.append(ScratchCard(card_id, win_numbers, played_numbers))

        if part == 1:
            for card in cards:
                score, nb_won_numbers = card.get_score()
                if nb_won_numbers == 0:
                    continue
                if part == 1:
                    total_part1 += score
                else:
                    total_part2 += score
        else:
            nb_cards_by_id = {}
            for card in cards:
                score, nb_won_numbers = card.get_score()
                if nb_cards_by_id.get(card.id) is None:
                    nb_cards_by_id[card.id] = 0
                nb_cards_by_id[card.id] += 1
                for i in range(card.id + 1, card.id + nb_won_numbers + 1):
                    if nb_cards_by_id.get(i) is None:
                        nb_cards_by_id[i] = 0
                    nb_cards_by_id[i] += nb_cards_by_id[card.id]

            total_part2 = Enumerable(nb_cards_by_id.values()).sum()

        if part == 1:
            return total_part1
        else:
            return total_part2

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 30
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
