import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def print_lines(lines, energized, cur):
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            if (y, x) == cur:
                print("X", end="", flush=True)
            elif (y, x) in energized:
                print("#", end="", flush=True)
            else:
                print(l, end="", flush=True)
        print()

def part1(lines):
    energized = []
    beams = []
    beams.append((0, 0, 0, 1))
    while any(beams):
        beam = beams.pop()
        y, x, dy, dx = beam

        if (y, x) not in energized:
            energized.append((y, x))
        print_lines(lines, energized, (y, x))
        print(f"energized: {len(energized)}")

        print(f"beam: {beam}")

        if y == 0 and dy == -1 or y == len(lines) - 1 and dy == 1:
            print("hit top or bottom")
        elif x == 0 and dx == -1 or x == len(lines[0]) - 1 and dx == 1:
            print("hit left or right")
        elif lines[y][x] == ".":
            print("hit empty, moving on...")
            beams.append((y+dy, x+dx, dy, dx))
        elif lines[y][x] == "/":
            print("hit /")
            if dy == 1:
                beams.append((y, x-1, 0, -1))
            elif dy == -1:
                beams.append((y, x+1, 0, 1))
            elif dx == 1:
                beams.append((y-1, x, -1, 0))
            elif dx == -1:
                beams.append((y+1, x, 1, 0))
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "\\":
            print("hit \\")
            if dy == 1:
                beams.append((y, x+1, 0, 1))
            elif dy == -1:
                beams.append((y, x-1, 0, -1))
            elif dx == 1:
                beams.append((y+1, x, 1, 0))
            elif dx == -1:
                beams.append((y-1, x, -1, 0))
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "|":
            print("hit |")
            if (dy == 1 or dy == -1) and dx == 0:
                print("considering empty... moving on...")
                beams.append((y + dy, x + dx, dy, dx))
            else:
                if y+1 < len(lines):
                    beams.append((y+1, x, 1, 0))
                if y-1 >= 0:
                    beams.append((y-1, x, -1, 0))

        elif lines[y][x] == "-":
            print("hit -")
            if (dx == 1 or dx == -1) and dy == 0:
                print("considering empty... moving on...")
                beams.append((y + dy, x + dx, dy, dx))
            else:
                if x+1 < len(lines[0]):
                    beams.append((y, x+1, 0, 1))
                if x-1 >= 0:
                    beams.append((y, x-1, 0, -1))
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
