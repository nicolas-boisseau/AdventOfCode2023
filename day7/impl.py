import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all
from day7.cards import Game, Hand

download_input_if_not_exists(2023)



def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        g = Game()
        for line in lines:
            split = line.split(" ")
            h = Hand(split[0], int(split[1]))

            g.add_hand(h)

        return g.total_score()

if __name__ == '__main__':

    level = 1
    expectedSampleResult = 6440
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
