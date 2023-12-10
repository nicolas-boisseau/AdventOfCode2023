import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


# https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
def DFS(G,v,seen=None,path=None):
    if seen is None: seen = []
    if path is None: path = [v]

    seen.append(v)

    paths = []
    for t in G[v]:
        if t not in seen:
            t_path = path + [t]
            paths.append(tuple(t_path))
            paths.extend(DFS(G, t, seen[:], t_path))
    return paths

def DFS2(g, source):
  s = []
  visited = set([])
  path = []
  s.append(source)
  while len(s) > 0:
    current = s.pop()
    if current in visited:
        continue
    visited.add(current)
    path.append(current)
    # do something with current
    for v in g[current]:
        s.append(v)
  return visited, path


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        in_bounds = lambda x, y: 0 <= x < len(lines[0]) and 0 <= y < len(lines)
        g = defaultdict(list)
        add_if_in_bounds = lambda node, x, y: g[node].append(f"{y}_{x}") if in_bounds(x, y) else None
        s = "0_0"

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                node = f"{y}_{x}"
                if char == "|":
                    add_if_in_bounds(node, x, y-1)
                    add_if_in_bounds(node, x, y+1)
                elif char == "-":
                    add_if_in_bounds(node, x-1, y)
                    add_if_in_bounds(node, x+1, y)
                elif char == "L":
                    add_if_in_bounds(node, x, y-1)
                    add_if_in_bounds(node, x+1, y)
                elif char == "J":
                    add_if_in_bounds(node, x, y-1)
                    add_if_in_bounds(node, x-1, y)
                elif char == "7":
                    add_if_in_bounds(node, x-1, y)
                    add_if_in_bounds(node, x, y+1)
                elif char == "F":
                    add_if_in_bounds(node, x+1, y)
                    add_if_in_bounds(node, x, y+1)
                #elif char == ".":
                elif char == "S":
                    if in_bounds(x, y-1) and (lines[y-1][x] == "|" or lines[y-1][x] == "7" or lines[y-1][x] == "F"):
                        add_if_in_bounds(node, x, y-1)
                    if in_bounds(x, y+1) and (lines[y+1][x] == "|" or lines[y+1][x] == "J" or lines[y+1][x] == "L"):
                        add_if_in_bounds(node, x, y+1)
                    elif in_bounds(x-1, y) and (lines[y][x-1] == "-" or lines[y][x-1] == "F" or lines[y][x-1] == "L"):
                        add_if_in_bounds(node, x-1, y)
                    elif in_bounds(x+1, y) and (lines[y][x+1] == "-" or lines[y][x+1] == "7" or lines[y][x+1] == "J"):
                        add_if_in_bounds(node, x+1, y)
                    s = node


        if part == 1:
            return int(len(DFS2(g, s)[1]) / 2)
        else:
            total = 0
            seen = set([])
            origin_path = [p for p in DFS2(g, s)[1]]
            # replace unconnected pipes

            for y, line in enumerate(lines):
                newLine = ""
                for x, char in enumerate(line):
                    if f"{y}_{x}" not in origin_path:
                        newLine += "."
                    else:
                        newLine += char
                lines[y] = newLine
            #print_with_current_position(lines, seen, 0, 0, origin_path)

            paths = []
            paths.append(origin_path)
            path_rev = origin_path.copy()
            path_rev.reverse()
            paths.append(path_rev)
            results = []


            for path in paths:
                seen = set([])

                for i in range (0, len(path), 1):
                    captured = capture("([0-9]+)_([0-9]+)", path[i])
                    x, y = int(captured[1]), int(captured[0])

                    captured = capture("([0-9]+)_([0-9]+)", path[(i + 1) % len(path)])
                    next_x, next_y = int(captured[1]), int(captured[0])
                    direction_x = next_x - x
                    direction_y = next_y - y

                    to_look = []

                    if lines[y][x] == "|" and direction_y == -1:
                        to_look.append((1, 0))
                    elif lines[y][x] == "|" and direction_y == 1:
                        to_look.append((-1, 0))
                    elif lines[y][x] == "-" and direction_x == -1:
                        to_look.append((0, -1))
                    elif lines[y][x] == "-" and direction_x == 1:
                        to_look.append((0, 1))
                    elif lines[y][x] == "L" and direction_x == 0 and direction_y == -1:
                        to_look.append((1, -1))
                    elif lines[y][x] == "L" and direction_x == 1 and direction_y == 0:
                        to_look.append((0, 1))
                    elif lines[y][x] == "J" and direction_x == -1 and direction_y == 0:
                        to_look.append((-1, -1))
                    elif lines[y][x] == "J" and direction_x == 0 and direction_y == -1:
                        to_look.append((1, 0))
                    elif lines[y][x] == "7" and direction_x == -1 and direction_y == 0:
                        to_look.append((0, -1))
                    elif lines[y][x] == "7" and direction_x == 0 and direction_y == 1:
                        to_look.append((-1, 1))
                    elif lines[y][x] == "F" and direction_x == 1 and direction_y == 0:
                        to_look.append((1, 1))
                    elif lines[y][x] == "F" and direction_x == 0 and direction_y == 1:
                        to_look.append((-1, 0))
                    elif lines[y][x] == "S":
                        if direction_y == 0 and direction_x == 1:  # moving right
                            to_look.append((0, 1))
                        elif direction_y == 0 and direction_x == -1:  # moving left
                            look_at_y = -1
                            look_at_x = 0
                            to_look.append((0, -1))
                        elif direction_y == 1 and direction_x == 0:  # moving down
                            look_at_y = 0
                            look_at_x = -1
                            to_look.append((-1, 0))
                        elif direction_y == -1 and direction_x == 0:  # moving up
                            to_look.append((1, 0))
                        #pass
                    else:
                        print("ERROR !")
                        return

                    # look at right neighbour only
                    for look_at_x, look_at_y in to_look:
                        to_look = f"{y+look_at_y}_{x+look_at_x}"
                        if to_look not in seen and in_bounds(x+look_at_x, y+look_at_y) and lines[y+look_at_y][x+look_at_x] == ".":
                            seen = propagate_tiles_non_recursive(lines, seen, x+look_at_x, y+look_at_y)

                print_with_current_position(lines, seen, x, y, path)
                results.append(len(seen))

            print(results)


            return min(results)


def propagate_tiles_non_recursive(lines, seen, x, y):
    in_bounds = lambda x, y: 0 <= x < len(lines[0]) and 0 <= y < len(lines)

    #print(f"propagating {x}, {y}")
    if not in_bounds(x, y):
        return
    if f"{y}_{x}" in seen:
        return
    if lines[y][x] != ".":
        return
    seen.add(f"{y}_{x}")

    to_propagate = []
    to_propagate.append((y, x))
    while len(to_propagate) > 0:
        cur_y, cur_x = to_propagate.pop()
        if f"{cur_y}_{cur_x-1}" not in seen and in_bounds(cur_x-1, cur_y) and lines[cur_y][cur_x-1] == ".":
            to_propagate.append((cur_y, cur_x-1))
        if f"{cur_y}_{cur_x+1}" not in seen and in_bounds(cur_x+1, cur_y) and lines[cur_y][cur_x+1] == ".":
            to_propagate.append((cur_y, cur_x+1))
        if f"{cur_y-1}_{cur_x}" not in seen and in_bounds(cur_x, cur_y-1) and lines[cur_y-1][cur_x] == ".":
            to_propagate.append((cur_y-1, cur_x))
        if f"{cur_y+1}_{cur_x}" not in seen and in_bounds(cur_x, cur_y+1) and lines[cur_y+1][cur_x] == ".":
            to_propagate.append((cur_y+1, cur_x))
        seen.add(f"{cur_y}_{cur_x}")
    return seen


def print_with_current_position(lines, seen, x, y, path):
    for yy, line in enumerate(lines):
        for xx, char in enumerate(line):
            if f"{yy}_{xx}" in seen:
                print("I", end="", flush=True)
            elif f"{yy}_{xx}" in path:
                print("#", end="", flush=True)
            elif xx == x and yy == y:
                print("X", end="", flush=True)
            else:
                print(char, end="")
        print("")
    print("")

if __name__ == '__main__':

    level = 1
    expectedSampleResult = 4
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
