import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

d_print = lambda *args, **kwargs: print(*args, **kwargs) if False else None


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


def part1(lines, start=(0, 0, 0, 1)):
    energized = []
    beams = []
    beams.append(start)
    already_seen = set()
    append_if_inbounds = lambda y, x, dy, dx: beams.append((y, x, dy, dx)) if 0 <= y < len(lines) and 0 <= x < len(
        lines[0]) else None
    while any(beams):
        beam = beams.pop()
        y, x, dy, dx = beam
        if (y, x, dy, dx) in already_seen:
            continue
        already_seen.add((y, x, dy, dx))

        if (y, x) not in energized:
            energized.append((y, x))
        # print_lines(lines, energized, (y, x))
        d_print(f"energized: {len(energized)}")

        d_print(f"beam: {beam}")

        if lines[y][x] == ".":
            d_print("hit empty, moving on...")
            append_if_inbounds(y + dy, x + dx, dy, dx)
        elif lines[y][x] == "/":
            d_print("hit /")
            if dy == 1:
                append_if_inbounds(y, x - 1, 0, -1)
            elif dy == -1:
                append_if_inbounds(y, x + 1, 0, 1)
            elif dx == 1:
                append_if_inbounds(y - 1, x, -1, 0)
            elif dx == -1:
                append_if_inbounds(y + 1, x, 1, 0)
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "\\":
            d_print("hit \\")
            if dy == 1:
                append_if_inbounds(y, x + 1, 0, 1)
            elif dy == -1:
                append_if_inbounds(y, x - 1, 0, -1)
            elif dx == 1:
                append_if_inbounds(y + 1, x, 1, 0)
            elif dx == -1:
                append_if_inbounds(y - 1, x, -1, 0)
            else:
                raise Exception("Impossible")
        elif lines[y][x] == "|":
            d_print("hit |")
            if (dy == 1 or dy == -1) and dx == 0:
                d_print("considering empty... moving on...")
                append_if_inbounds(y + dy, x + dx, dy, dx)
            else:
                if y + 1 < len(lines):
                    append_if_inbounds(y + 1, x, 1, 0)
                if y - 1 >= 0:
                    append_if_inbounds(y - 1, x, -1, 0)

        elif lines[y][x] == "-":
            d_print("hit -")
            if (dx == 1 or dx == -1) and dy == 0:
                d_print("considering empty... moving on...")
                append_if_inbounds(y + dy, x + dx, dy, dx)
            else:
                if x + 1 < len(lines[0]):
                    append_if_inbounds(y, x + 1, 0, 1)
                if x - 1 >= 0:
                    append_if_inbounds(y, x - 1, 0, -1)
        elif y == 0 and dy == -1 or y == len(lines) - 1 and dy == 1:
            d_print("hit top or bottom")
        elif x == 0 and dx == -1 or x == len(lines[0]) - 1 and dx == 1:
            d_print("hit left or right")
        else:
            raise Exception("Impossible")

    return len(energized)


def part2(lines):
    max_energy = 0
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            # edges only
            if y != 0 and y != len(lines) - 1 and x != 0 and x != len(lines[0]) - 1:
                continue

            dx = dy = 0
            # corners
            if y == 0 and x == 0:
                max_energy = max(max_energy, part1(lines, (y, x, 1, 0)))
                max_energy = max(max_energy, part1(lines, (y, x, 0, 1)))
            elif y == len(lines) - 1 and x == 0:
                max_energy = max(max_energy, part1(lines, (y, x, -1, 0)))
                max_energy = max(max_energy, part1(lines, (y, x, 0, 1)))
            elif y == 0 and x == len(lines[0]) - 1:
                max_energy = max(max_energy, part1(lines, (y, x, 1, 0)))
                max_energy = max(max_energy, part1(lines, (y, x, 0, -1)))
            elif y == len(lines) - 1 and x == len(lines[0]) - 1:
                max_energy = max(max_energy, part1(lines, (y, x, -1, 0)))
                max_energy = max(max_energy, part1(lines, (y, x, 0, -1)))
            else:
                if y == 0:
                    dy = 1
                elif y == len(lines) - 1:
                    dy = -1
                elif x == 0:
                    dx = 1
                elif x == len(lines[0]) - 1:
                    dx = -1
                max_energy = max(max_energy, part1(lines, (y, x, dy, dx)))
    return max_energy


if __name__ == '__main__':

    part = 2
    expectedSampleResult = 51

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
