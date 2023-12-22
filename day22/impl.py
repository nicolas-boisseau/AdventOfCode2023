import os.path
import heapq
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def extract(lines):
    cubes = []
    for i, line in enumerate(lines):
        cube_positions = line.split("~")
        cube_pos_1 = cube_positions[0].split(",")
        cube_pos_2 = cube_positions[1].split(",")
        start = (int(cube_pos_1[0]), int(cube_pos_1[1]), int(cube_pos_1[2]))
        end = (int(cube_pos_2[0]), int(cube_pos_2[1]), int(cube_pos_2[2]))
        cube = (start, end)
        # for z in range(start[2], end[2]+1):
        #     for y in range(start[1], end[1]+1):
        #         for x in range(start[0], end[0]+1):
        #             cube[(x, y, z)] = True

        cubes.append(cube)
    return cubes

def intersect_another_cube(cube, other_cube):
    for z in range(cube[0][2], cube[1][2]+1):
        for y in range(cube[0][1], cube[1][1]+1):
            for x in range(cube[0][0], cube[1][0]+1):
                for z2 in range(other_cube[0][2], other_cube[1][2]+1):
                    for y2 in range(other_cube[0][1], other_cube[1][1]+1):
                        for x2 in range(other_cube[0][0], other_cube[1][0]+1):
                            if x == x2 and y == y2 and z == z2:
                                return True
    return False

def print_from_y_perspective(cubes):
    maxX = max([max(max(cube[0][0], cube[1][0]) for cube in cubes)])
    maxZ = max([max(max(cube[0][2], cube[1][2]) for cube in cubes)])

    for z in range(maxZ+1):
        for y in range(maxX+1):
            for i, cube in enumerate(cubes):
                if cube[0][1] <= y <= cube[1][1] and cube[0][2] <= z <= cube[1][2]:
                    print(i, end="")
                    break
            else:
                print(".", end="")
        print()
    print()

def part1(lines):
    cubes = extract(lines)
    cubes_q = heapq.heapify(cubes, key=lambda cube: min(cube[0][2], cube[1][2]))

    # lets let cubes fall on Z axis
    has_not_moved = defaultdict(bool)
    final_cubes = []
    print_from_y_perspective(cubes)
    while all([not has_not_moved[cube] for cube in cubes]):

        next_cube = heapq.heappop(cubes_q)

        # check if cube can fall
        if next_cube[0][2] <= 1:
            # cube already on the ground
            has_not_moved[next_cube] = True
            final_cubes.append(next_cube)
            continue

        # check if cube can fall
        can_fall = True
        while can_fall:
            next_cube[0][2] -= 1
            next_cube[1][2] -= 1
            for other_cube in cubes:
                if intersect_another_cube(next_cube, other_cube):
                    can_fall = False
                    break
            if can_fall:
                has_not_moved[next_cube] = False
            else:
                next_cube[0][2] += 1
                next_cube[1][2] += 1
                has_not_moved[next_cube] = True
                final_cubes.append(next_cube)

    print_from_y_perspective(final_cubes)






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
