import os.path
from functools import lru_cache
from random import random

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


# BIG THANKS @Tavahiura Sang ! Saving my brain :)
# https://github.com/tavash/advent-of-code/blob/main/2023/12/main.py

@lru_cache # 💯🔥 memoize => https://wellsr.com/python/optimizing-recursive-functions-with-python-memoization/
def get_arrangements(row,group):
    row = row.lstrip('.') # supprime les '.' au début de la ligne
    # debug
    # print (row, group)
    # '', ()
    # '', (1,)
    # combinaison trouvée si group est vide et row est vide
    if len(row) == 0:
        if len(group) == 0:
            return 1
        return 0

    # combinaison trouvée si group est vide et row ne contient pas de '#'
    if len(group) == 0:
        if '#' not in row:
            return 1
        return 0

    # row commence par '#'
    if row.startswith('#'):
        current_group = group[0]

        # ex: "##" (4,) => impossible
        if len(row) < current_group:
            return 0

        # ex: "##.???" (3,1)
        if '.' in row[:current_group]:
            return 0

        # combinaison trouvée si taille row == current_group et group n'a qu'un élément
        if len(row) == current_group:
            if len(group) == 1:
                return 1
            return 0

        # la séparation d'un spring doit être par un '.' ou '?'
        if row[current_group] == '#':
            return 0

        # sinon on continue avec le reste de la ligne et le reste du group
        return get_arrangements(row[current_group+1:], group[1:])

    # commence forcément par un '?'
    # si "?###?" (4,) alors
    #   -> "####?" (4,)
    #   -> ".###?" (4,)
    return get_arrangements(row.replace("?", "#", 1), group) + get_arrangements(row[1:], group)

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    result2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        part1_results = []
        for i, line in enumerate(lines):
            splitted = line.split(" ")
            spring_row = splitted[0]
            records_raw = splitted[1]

            records = [int(d) for d in records_raw.split(",")]

            if part == 1:
                mutations = find_mutations(spring_row, records)
                part1_results.append(len(mutations))

            if part == 2:

                # spring_row2 = f"{spring_row}?"
                spring_row = multiply_sequence(spring_row, "?", 5)
                # records_raw2 = records_raw #multiply_sequence(records_raw, ",", 2)
                records_raw = multiply_sequence(records_raw, ",", 5)
                #
                records = [int(d) for d in records_raw.split(",")]

                result2 += get_arrangements(spring_row, tuple(records))

                # records2 = [int(d) for d in records_raw2.split(",")]
                #
                # # print(f"row = '{spring_row}', records={records}")
                #
                # mutations = find_mutations(spring_row, records)
                # mutations2 = find_mutations(spring_row2, records2)
                # # print(f"row = '{spring_row}', nb_mutations={len(mutations)}")
                #
                # part2_results.append(len(mutations))
                # part2_results2.append(len(mutations2))
                # print(f"1. = '{spring_row}', part1={part1_results[i]}, x+?+x={part2_results[i]}")
                # print(f"2. = '{spring_row2}', part1={part1_results[i]}, x+?={part2_results2[i]}")
                #
                # a1 = part1_results[i]
                # b1 = part2_results[i]
                # a2 = part1_results[i]
                # b2 = part2_results2[i]
                #
                # res1 = (b1 / a1)**4 * a1
                # res2 = (b2+(b2*a2) / a1)**4 * a1
                #
                # print(f"1. = ({part2_results[i]} / {part1_results[i]})**4 * ({part1_results[i]})) = {res1}")
                # print(f"2. = (({part2_results2[i]}+({part2_results2[i]}*{part1_results[i]}) / {part1_results[i]})**4 * ({part1_results[i]}) = {res2}")
                # part2_results[i] = res1
                # part2_results2[i] = res2



        return int(sum(part1_results)) if part == 1 else result2

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
    possibles_mutations = [m for m in list(get_mutations_for(len(joker_positions))) if "##" not in m]
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

    level = 2
    expectedSampleResult = 525152
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
