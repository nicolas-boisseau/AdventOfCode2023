import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)


directions = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}

directions2 = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def print_grid(grid):
    minY = min([p[0] for p in grid])
    minX = min([p[1] for p in grid])
    maxY = max([p[0] for p in grid])
    maxX = max([p[1] for p in grid])
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (y, x) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()

def fill_inside(grid, instructions):
    first_instr = instructions[0]
    # look at right
    if first_instr[0] == "U":
        propagate_non_recursive(grid, directions["U"][0], directions["U"][1] + 1)
    elif first_instr[0] == "D":
        propagate_non_recursive(grid, directions["D"][0], directions["D"][1] - 1)
    elif first_instr[0] == "L":
        propagate_non_recursive(grid, directions["L"][0] - 1, directions["L"][1])
    elif first_instr[0] == "R":
        propagate_non_recursive(grid, directions["R"][0] + 1, directions["R"][1])

def propagate_non_recursive(grid, x, y):
    minY = min([p[0] for p in grid])
    minX = min([p[1] for p in grid])
    maxY = max([p[0] for p in grid])
    maxX = max([p[1] for p in grid])
    in_bounds = lambda x, y: minX <= x < maxX and minY <= y < maxY

    #print(f"propagating {x}, {y}")
    if not in_bounds(x, y):
        return
    if (y, x) in grid:
        return

    to_propagate = []
    to_propagate.append((y, x))
    while len(to_propagate) > 0:
        cur_y, cur_x = to_propagate.pop()
        if (cur_y, cur_x-1) not in grid and in_bounds(cur_x-1, cur_y):
            to_propagate.append((cur_y, cur_x-1))
        if (cur_y, cur_x+1) not in grid and in_bounds(cur_x+1, cur_y):
            to_propagate.append((cur_y, cur_x+1))
        if (cur_y-1, cur_x) not in grid and in_bounds(cur_x, cur_y-1):
            to_propagate.append((cur_y-1, cur_x))
        if (cur_y+1, cur_x) not in grid and in_bounds(cur_x, cur_y+1):
            to_propagate.append((cur_y+1, cur_x))
        if (cur_y, cur_x) not in grid:
            grid[(cur_y, cur_x)] = 1
    return grid

def draw(grid, instructions, fill=True):
    x = y = 0
    grid[(y, x)] = 1
    for instr in instructions:
        direction = directions[instr[0]]
        for i in range(instr[1]):
            y += direction[0]
            x += direction[1]
            if (y, x) not in grid:
                grid[(y, x)] = 1

    print(f"before fill: {len(grid)}")
    if fill:
        fill_inside(grid, instructions)

    return len(grid)

# https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area#Python
def area_by_shoelace(x, y):
    "Assumes x,y points go around the polygon in one direction"
    return abs( sum(i * j for i, j in zip(x, y[1:] + y[:1]))
               -sum(i * j for i, j in zip(x[1:] + x[:1], y))) / 2

def draw2(instructions):
    x = y = 0
    points = [(x, y)]
    total_distance = 0
    for instr in instructions:
        direction = directions[instr[0]]
        dy = (instr[1] * direction[0])
        dx = (instr[1] * direction[1])
        total_distance += abs(dy + dx)
        y = y + dy
        x = x + dx
        points.append((x, y))

    xx, yy = zip(*points)
    return int(area_by_shoelace(xx, yy) + total_distance / 2) + 1



def part1(lines):
    instructions = []
    grid = {}
    for line in lines:
        splitted = line.split(" ")

        direction = splitted[0]
        distance = int(splitted[1])

        instructions.append((direction, distance))

    #return draw(grid, instructions)
    return draw2(instructions)


def part2(lines):
    instructions = []
    for line in lines:
        splitted = line.split(" ")

        hexa = splitted[2]

        direction = directions2[hexa[7]]
        distance = int(hexa[2:7], 16)

        instructions.append((direction, distance))

    return draw2(instructions)


if __name__ == '__main__':

    part = 1
    expectedSampleResult = 62

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
