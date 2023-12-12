import os.path
from random import random

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        total = 0
        for line in lines:
            splitted = line.split(" ")
            spring_row = splitted[0]
            records = [int(d) for d in splitted[1].split(",")]

            #print(f"row = '{spring_row}', records={records}")


            if "?" in spring_row:
                mutations = find_mutations(spring_row, records)
                #print(f"row = '{spring_row}', nb_mutations={len(mutations)}")

                total += len(mutations)

        return total

def find_joker_positions(spring_row):
    jokers = []
    for i in range(len(spring_row)):
        if spring_row[i] == "?":
            jokers.append(i)
    return jokers

def get_mutations_for(n):
    for i in range(2 ** n):
        yield bin(i)[2:].zfill(n).replace("0", ".").replace("1", "#")

def find_mutations(spring_row, records):
    joker_positions = find_joker_positions(spring_row)
    correct_mutations = []
    possibles_mutations = list(get_mutations_for(len(joker_positions)))
    for mutation in possibles_mutations:
        current = ""
        for i, c in enumerate(spring_row):
            if i in joker_positions:
                current += mutation[joker_positions.index(i)]
            else:
                current += c
        if is_match_record(current, records):
            correct_mutations.append(current)
    return correct_mutations

def is_match_record(spring_row, records):
    r = []
    current = 0
    for c in spring_row:
        if c == "#":
            current += 1
        else:
            if current > 0:
                r.append(current)
            current = 0
    if current > 0:
        r.append(current)
    return r == records



if __name__ == '__main__':

    level = 1
    expectedSampleResult = 21
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
