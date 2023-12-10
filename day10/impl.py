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
  s.append(source)
  while len(s) > 0:
    current = s.pop()
    if current in visited:
        continue
    visited.add(current)
    # do something with current
    for v in g[current]:
        s.append(v)
  return visited

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
                    if in_bounds(x-1, y) and (lines[y][x-1] == "-" or lines[y][x-1] == "F" or lines[y][x-1] == "L"):
                        add_if_in_bounds(node, x-1, y)
                    if in_bounds(x+1, y) and (lines[y][x+1] == "-" or lines[y][x+1] == "7" or lines[y][x+1] == "J"):
                        add_if_in_bounds(node, x+1, y)
                    s = node


        #print(DFS2(g, s))

        return int(len(DFS2(g, s)) / 2)




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
