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
        for line in lines[0:1]:
            splitted = line.split(" ")
            spring_row = splitted[0]
            records_raw = splitted[1]
            if part == 2:
                spring_row = multiply_sequence(spring_row, "?", 5)
                records_raw = multiply_sequence(records_raw, ",", 5)
            records = [int(d) for d in records_raw.split(",")]

            #print(f"row = '{spring_row}', records={records}")

            if "?" in spring_row:
                mutations = find_mutations(spring_row, records)
                #print(f"row = '{spring_row}', nb_mutations={len(mutations)}")

                total += len(mutations)

        return total

def compute_simplest(records):
    current = ""
    for i, r in enumerate(records):
        current += "#" * r
        if i < len(records) - 1:
            current += "."
    return current

def compute_possibilities(records, max_length):
    simplest = compute_simplest(records)
    possibilities = [simplest + "."*(max_length - len(simplest))]
    empty_positions = find_char_positions(simplest, ".")
    empty_positions.append(len(simplest)-1)
    to_fill = max_length - len(simplest)

    append_if_valid = lambda p: possibilities.append(p) if is_match_record(p, records) else None

    for i in range(to_fill):
        for j in range(i, to_fill):
            if empty_positions[i] == len(simplest)-1:
                possibilities.append(possibilities[j][:empty_positions[i]] + "."*j)
            possibilities.append(possibilities[j][:empty_positions[i]] + "."*j + possibilities[j][empty_positions[i]+1:])





def multiply_sequence(spring_row, separator, n):
    return separator.join([spring_row for _ in range(n)])

def find_char_positions(spring_row, char):
    jokers = []
    for i in range(len(spring_row)):
        if spring_row[i] == char:
            jokers.append(i)
    return jokers

def get_mutations_for(n):
    for i in range(2 ** n):
        yield bin(i)[2:].zfill(n).replace("0", ".").replace("1", "#")

def find_mutations(spring_row, records):
    joker_positions = find_char_positions(spring_row, "?")
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
