import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all
from day11.astar_test import BasicAStar

download_input_if_not_exists(2023)

def findGalaxiesPositions(lines):
    galaxies = []
    index = 1
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((index, (x, y)))
                index += 1
    return galaxies


def expand_rows(lines):
    to_insert = []
    for r, line in enumerate(lines):
        if Enumerable(line).all(lambda x: x == "."):
            to_insert.append(r)

    to_insert.reverse()
    for r in to_insert:
        lines.insert(r, "." * len(lines[0]))

    return lines

def expand_columns(lines):
    to_insert = []
    for c, _ in enumerate(lines[0]):
        if (Enumerable([line[c] for line in lines]).all(lambda x: x == ".")):
            to_insert.append(c)

    to_insert.reverse()
    for r_to_insert in to_insert:
        for i, line in enumerate(lines):
            lines[i] = line[:r_to_insert] + "." + line[r_to_insert:]

    return lines


def print_lines(lines):
    for line in lines:
        print(line)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        lines = expand_rows(lines)
        lines = expand_columns(lines)
        #print_lines(lines)
        galaxies = findGalaxiesPositions(lines)
        print(f"nb galaxies: {len(galaxies)}")

        nodes = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                node_key = f"{x},{y}"
                nodes[node_key] = []
                if x > 0:
                    nodes[node_key].append((f"{x-1},{y}", 1))
                if y > 0:
                    nodes[node_key].append((f"{x},{y-1}", 1))
                if x < len(line)-1:
                    nodes[node_key].append((f"{x+1},{y}", 1))
                if y < len(lines)-1:
                    nodes[node_key].append((f"{x},{y+1}", 1))

        astar = BasicAStar(nodes)

        pairs = {}
        for i_g, galaxy in enumerate(galaxies):
            for j_g, other_galaxy in enumerate(galaxies):
                if i_g != j_g and ((galaxy[0], other_galaxy[0]) not in pairs) and ((other_galaxy[0], galaxy[0]) not in pairs):
                    path = astar.astar(f"{galaxy[1][0]},{galaxy[1][1]}", f"{other_galaxy[1][0]},{other_galaxy[1][1]}")
                    path = list(path)
                    pairs[(galaxy[0], other_galaxy[0])] = len(path)-1
                print(f"Computed galaxies: {len(pairs)}")

    return sum(pairs.values())


if __name__ == '__main__':

    level = 1
    expectedSampleResult = 374
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
