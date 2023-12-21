import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def extract(lines):
    g = defaultdict(bool)
    s = ()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                g[(y, x, 0, 0)] = False
            elif c == "S":
                s = (y, x, 0, 0)
                g[(y, x, 0, 0)] = False
    return g, s

def print_grid(lines, g, s):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if (y, x) in g and g[(y, x)]:
                print("O", end="")
            else:
                print(c, end="")
        print()
    print(flush=True)

def part1(lines, max_steps=6):
    g, s = extract(lines)
    steps = [s]
    for i in range(0, max_steps):
        next_steps = []
        while steps:
            step = steps.pop(0)
            up = (step[0]-1, step[1], step[2], step[3])
            down = (step[0]+1, step[1], step[2], step[3])
            left = (step[0], step[1]-1, step[2], step[3])
            right = (step[0], step[1]+1, step[2], step[3])

            if up in g and not g[up]:
                g[up] = True
                next_steps.append(up)
            if down in g and not g[down]:
                g[down] = True
                next_steps.append(down)
            if left in g and not g[left]:
                g[left] = True
                next_steps.append(left)
            if right in g and not g[right]:
                g[right] = True
                next_steps.append(right)
        steps = next_steps
        # reset grid
        for k in g:
            g[k] = False
        #print_grid(lines, g, s)

    return len(steps)

def part2(lines, max_steps=6):
    g, s = extract(lines)
    steps = [s]
    for i in range(0, max_steps):
        next_steps = []
        while steps:
            step = steps.pop(0)
            up = (step[0] - 1, step[1], step[2], step[3])
            down = (step[0] + 1, step[1], step[2], step[3])
            left = (step[0], step[1] - 1, step[2], step[3])
            right = (step[0], step[1] + 1, step[2], step[3])

            # fix out of range pos
            if up[0]==-1:
                up = (len(lines)-1, up[1], up[2]-1, up[3])
            if down[0]==len(lines):
                down = (0, down[1], down[2]+1, down[3])
            if left[1]==-1:
                left = (left[0], len(lines[0])-1, left[2], left[3]-1)
            if right[1]==len(lines[0]):
                right = (right[0], 0, right[2], right[3]+1)

            if (up[0], up[1], 0, 0) in g and not g[up]:
                g[up] = True
                next_steps.append(up)
            if (down[0], down[1], 0, 0) in g and not g[down]:
                g[down] = True
                next_steps.append(down)
            if (left[0], left[1], 0, 0) in g and not g[left]:
                g[left] = True
                next_steps.append(left)
            if (right[0], right[1], 0, 0) in g and not g[right]:
                g[right] = True
                next_steps.append(right)
        steps = next_steps
        # reset grid
        for k in g:
            g[k] = False
        #print_grid(lines, g, s)

    return len(steps)


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
