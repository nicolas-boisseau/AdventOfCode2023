import math
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


def get_rows_to_expand(lines):
    to_insert = []
    for r, line in enumerate(lines):
        if Enumerable(line).all(lambda x: x == "."):
            to_insert.append(r)

    # to_insert.reverse()
    # for r in to_insert:
    #     lines.insert(r, "." * len(lines[0]))
    #
    # return lines
    return to_insert

def get_cols_to_expand(lines):
    to_insert = []
    for c, _ in enumerate(lines[0]):
        if (Enumerable([line[c] for line in lines]).all(lambda x: x == ".")):
            to_insert.append(c)

    # to_insert.reverse()
    # for r_to_insert in to_insert:
    #     for i, line in enumerate(lines):
    #         lines[i] = line[:r_to_insert] + "." + line[r_to_insert:]

    return to_insert


def print_lines(lines):
    for line in lines:
        print(line)


def process(part, filename, expand=1):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        rows_to_expand = get_rows_to_expand(lines)
        cols_to_expand = get_cols_to_expand(lines)

        to_expand = 1
        if part == 2:
            to_expand = expand

        #print_lines(lines)
        galaxies = findGalaxiesPositions(lines)
        print(f"nb galaxies: {len(galaxies)}")

        # nodes = {}
        # for y, line in enumerate(lines):
        #     for x, char in enumerate(line):
        #         node_key = f"{x},{y}"
        #         nodes[node_key] = []
        #         if x > 0:
        #             nodes[node_key].append((f"{x-1},{y}", 1))
        #         if y > 0:
        #             nodes[node_key].append((f"{x},{y-1}", 1))
        #         if x < len(line)-1:
        #             nodes[node_key].append((f"{x+1},{y}", 1))
        #         if y < len(lines)-1:
        #             nodes[node_key].append((f"{x},{y+1}", 1))

        #astar = BasicAStar(nodes)

        pairs = {}
        for i_g in range(0, len(galaxies)):
            for j_g in range(i_g+1, len(galaxies)):
                galaxy = galaxies[i_g]
                other_galaxy = galaxies[j_g]
                if i_g != j_g and ((galaxy[0], other_galaxy[0]) not in pairs) and ((other_galaxy[0], galaxy[0]) not in pairs):

                    x1 = galaxy[1][0]
                    y1 = galaxy[1][1]
                    x2 = other_galaxy[1][0]
                    y2 = other_galaxy[1][1]

                    toadd_y2 = toadd_y1 = 0
                    for expand_row in rows_to_expand:
                        if y1 < y2 and y1 < expand_row < y2:
                            toadd_y2 += (to_expand-1 if to_expand > 1 else 1)
                        elif y1 > y2 and y2 < expand_row < y1:
                            toadd_y1 += (to_expand-1 if to_expand > 1 else 1)
                    y2 += toadd_y2
                    y1 += toadd_y1

                    toadd_x2 = toadd_x1 = 0
                    for expand_col in cols_to_expand:
                        if x1 < x2 and x1 < expand_col < x2:
                            toadd_x2 += (to_expand-1 if to_expand > 1 else 1)
                        elif x1 > x2 and x2 < expand_col < x1:
                            toadd_x1 += (to_expand-1 if to_expand > 1 else 1)
                    x2 += toadd_x2
                    x1 += toadd_x1

                    pairs[(galaxy[0], other_galaxy[0])] = abs(x2 - x1) + abs(y2 - y1)




                    # else:
                    #     path = astar.astar(f"{galaxy[1][0]},{galaxy[1][1]}", f"{other_galaxy[1][0]},{other_galaxy[1][1]}")
                    #     path = list(path)
                    #     pairs[(galaxy[0], other_galaxy[0])] = len(path)-1
                #print(f"Computed galaxies: {len(pairs)}")

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
