import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines
from day23.astar_test import BasicAStar

download_input_if_not_exists(2023)

def part1(lines):
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

    return 0

def part2(lines):
    return 4


if __name__ == '__main__':

    part = 1
    expectedSampleResult = -1

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
