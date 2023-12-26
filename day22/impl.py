import os.path
import heapq
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def extract(lines):
    cubes = []
    for id, line in enumerate(lines):
        cube_positions = line.split("~")
        cube_pos_1 = cube_positions[0].split(",")
        cube_pos_2 = cube_positions[1].split(",")
        x1, y1, z1 = tuple(map(int, cube_pos_1))
        x2, y2, z2 = tuple(map(int, cube_pos_2))
        cube = ({}, id)
        if z2 < z1:
            x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        for z in range(z1, z2+1):
            for y in range(y1, y2+1):
                for x in range(x1, x2+1):
                    cube[0][(x, y, z)] = True

        cubes.append(cube)

    return sorted(cubes, key=lambda c: min_Z(c))


names = defaultdict(str)
names.update({
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G"
})

def intersect_another_cube(cube, other_cube):
    return any([pos in other_cube[0] for pos in cube[0]])

def min_Z(cube):
    return min([zz for (xx, yy, zz) in cube[0].keys()])

def max_Z(cube):
    return max([zz for (xx, yy, zz) in cube[0].keys()])

def min_X(cube):
    return min([xx for (xx, yy, zz) in cube[0].keys()])

def max_X(cube):
    return max([xx for (xx, yy, zz) in cube[0].keys()])

def min_Y(cube):
    return min([yy for (xx, yy, zz) in cube[0].keys()])

def max_Y(cube):
    return max([yy for (xx, yy, zz) in cube[0].keys()])

def print_from_y_perspective(cubes):
    maxX = max([max(max_X(cube) for cube in cubes)])
    maxZ = max([max(max_Z(cube) for cube in cubes)])

    for z in range(maxZ, -1, -1):
        for x in range(maxX+1):
            cube_here = []
            for i, cube in enumerate(cubes):
                if (x, z) in [(xx, zz) for xx,yy,zz in cube[0].keys()]:
                    cube_here.append(names[cube[1]])
            if len(cube_here) == 0:
                print(".", end="")
            else:
                print(cube_here[0] if len(cube_here)==1 else "?", end="")
        print()
    print()

def print_from_x_perspective(cubes):
    maxY = max([max(max_Y(cube) for cube in cubes)])
    maxZ = max([max(max_Z(cube) for cube in cubes)])

    for z in range(maxZ, -1, -1):
        for y in range(maxY+1):
            cube_here = []
            for i, cube in enumerate(cubes):
                if (y, z) in [(yy, zz) for xx,yy,zz in cube[0].keys()]:
                    cube_here.append(names[cube[1]])
            if len(cube_here) == 0:
                print(".", end="")
            else:
                print(cube_here[0] if len(cube_here) == 1 else "?", end="")
        print()
    print()

supporting = defaultdict(list)
supported_by = defaultdict(list)

def fall(cubes, debug=False):
    global supporting, supported_by

    new_cubes = []
    while cubes:
        current_cube = cubes.pop(0)
        if debug:
            print(f"current_cube = {names[current_cube[1]]}")

        # check if cube can fall
        can_fall = True
        while can_fall:
            if min_Z(current_cube) <= 1:
                # cube already on the ground
                break

            new_current_cube_moins_1_Z = ({(x,y,z-1):v for (x,y,z), v in current_cube[0].items()}, current_cube[1])

            for other_cube in new_cubes:
                if intersect_another_cube(new_current_cube_moins_1_Z, other_cube):
                    can_fall = False
                    if current_cube[1] not in supporting[other_cube[1]]:
                        supporting[other_cube[1]].append(current_cube[1])

                    if other_cube[1] not in supported_by[current_cube[1]]:
                        supported_by[current_cube[1]].append(other_cube[1])
            if can_fall:
                if debug:
                    print(f"Cube {names[current_cube[1]]} falling -1 !")
                current_cube = new_current_cube_moins_1_Z

        # replace cube in cubes
        new_cubes.append(current_cube)


    return new_cubes


def get_removable_cube_ids(cubes, supporting, supported_by):
    removable = {}
    for cube in cubes:
        blocks, id = cube
        if len(supporting[id]) == 0:
            removable[id] = True
            continue
        else:
            if all([len(supported_by[supporting_]) > 1 for supporting_ in supporting[id]]):
                removable[id] = True
                continue
    return removable


def part1(lines, debug=False):
    global supporting, supported_by

    cubes = extract(lines)
    if debug:
        print_from_y_perspective(cubes)
        print_from_x_perspective(cubes)

    cubes = fall(cubes, debug)

    print("After falling :")
    if debug:
        print_from_y_perspective(cubes)
        print_from_x_perspective(cubes)

    print(f"supporting = {supporting}")
    print(f"supported_by = {supported_by}")

    removable = get_removable_cube_ids(cubes, supporting, supported_by)

    removable_str = [ f"{id} ({names[id]})" for id in removable.keys()]
    print(f"removable = {removable_str}")

    return len(removable)



def part2(lines):
    global supporting, supported_by

    cubes = fall(extract(lines), False)

    removable = get_removable_cube_ids(cubes, supporting, supported_by)

    total_fall_if_removed = 0
    for c in [cube for cube in cubes if cube[1] not in removable]:
        blocks, id = c
        fallen = {}
        falling = [id]
        current_total_falling = 0
        while falling:
            current_cube_id = falling.pop(0)
            fallen[current_cube_id] = True
            current_total_falling += 1
            for supporting_ in [s for s in supporting[current_cube_id] if all([supp_by in fallen for supp_by in supported_by[s]])]:
                falling.append(supporting_)

        total_fall_if_removed += current_total_falling-1

    return total_fall_if_removed





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
