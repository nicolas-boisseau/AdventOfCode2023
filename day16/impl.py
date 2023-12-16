import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def print_lines(lines, energized):
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if (y, x) in energized:
                print("#", end="", flush=True)
            else:
                print(l, end="", flush=True)
        print()

def part1(lines):
    energized = []
    last_energized_measures = []
    no_new_energy = 0
    beams = {}
    beams["0"] = ("0", 0, 0, 0, 1, True)
    while any([b for b in beams.values() if b[5]]):
        beam = [b for b in beams.values() if b[5]][0]
        id, y, x, dy, dx, enabled = beam

        if (y, x) not in energized:
            energized.append((y, x))
        print_lines(lines, energized)

        last_energized_measures.append(len(energized))
        if len(last_energized_measures) > 2 and last_energized_measures[-1] == last_energized_measures[-2]:
            print("no new energized")
            no_new_energy += 1
            if no_new_energy > 100:
                print_lines(lines, energized)
                return len(energized)
        else:
            no_new_energy = 0
        print(f"energized: {len(energized)}")
        print(f"beam: {beam}")
        if not enabled:
            print("dead")
        elif y == 0 and dy == -1 or y == len(lines) - 1 and dy == 1:
            print("hit top or bottom")
            beams[id] = (id, y, x, dy, dx, False)
        elif x == 0 and dx == -1 or x == len(lines[0]) - 1 and dx == 1:
            print("hit left or right")
            beams[id] = (id, y, x, dy, dx, False)
        elif lines[y][x] == ".":
            print("hit empty")
            beams[id] = (id, y+dy, x+dx, dy, dx, True)
        elif lines[y][x] == "/":
            print("hit /")
            if dy == 1:
                beams[id] = (id, y, x-1, 0, -1, True)
            elif dy == -1:
                beams[id] = (id, y, x+1, 0, 1, True)
            elif dx == 1:
                beams[id] = (id, y-1, x, -1, 0, True)
            elif dx == -1:
                beams[id] = (id, y+1, x, 1, 0, True)
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "\\":
            print("hit \\")
            if dy == 1:
                beams[id] = (id, y, x+1, 0, 1, True)
            elif dy == -1:
                beams[id] = (id, y, x-1, 0, -1, True)
            elif dx == 1:
                beams[id] = (id, y+1, x, 1, 0, True)
            elif dx == -1:
                beams[id] = (id, y-1, x, -1, 0, True)
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "|":
            print("hit |")
            if (dy == 1 or dy == -1) and dx == 0:
                print("considering empty...")
                beams[id] = (id, y+dy, y+dx, dy, dx, True)
            else:
                beams[id] = (id, x, y, dy, dx, False)
                id_up = f"{id}_{y-1}_{x}_up"
                id_down = f"{id}_{y+1}_{x}_down"
                beams[id_up] = (id_up, y-1, x, 1, 0, True)
                beams[id_down] = (id_down, y+1, x, -1, 0, True)

        elif lines[y][x] == "-":
            print("hit -")
            if (dx == 1 or dx == -1) and dy == 0:
                print("considering empty...")
                beams[id] = (id, y+dy, x+dx, dy, dx, True)
            else:
                beams[id] = (id, x, y, dy, dx, False)
                id_left = f"{id}_{y}_{x-1}_left"
                id_right = f"{id}_{y}_{x+1}_right"
                beams[id_left] = (id_left, y, x+1, 0, 1, True)
                beams[id_right] = (id_right, y, x-1, 0, -1, True)
        else:
            raise Exception("Impossible")
    print_lines(lines, energized)
    return len(energized)

def part2(lines):
    return 4


if __name__ == '__main__':

    part = 1
    expectedSampleResult = 46

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
