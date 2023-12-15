import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)

def find_all(s, c):
    idx = s.find(c)
    while idx != -1:
        yield idx
        idx = s.find(c, idx + 1)

def get_balls_positions(lines):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "O":
                yield y, x

def print_lines(lines):
    for line in lines:
        for l in line:
            print(l, end="", flush=True)
        print()

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        balls = get_balls_positions(lines)

        #print(balls)
        print(lines == lines.copy())
        prev = lines
        turns = ["N"]
        nb_cycle = 1
        if part == 2:
            turns = ["N", "W", "S", "E"]
            nb_cycle = 1000
        turn = 0
        cycles = {}
        cycle = 0
        all_cycles = []
        for i in range(len(turns) * nb_cycle):
            while True:
                new = prev.copy()
                balls = get_balls_positions(new)
                for ball in balls:
                    y, x = ball

                    # move up if possible and up is not "#"
                    if turns[turn]=="N" and y > 0 and new[y-1][x] != "#" and new[y-1][x] != "O":
                        new[y-1] = new[y-1][:x] + "O" + new[y-1][x+1:]
                        new[y] = new[y][:x] + "." + new[y][x+1:]
                    elif turns[turn]=="W" and x > 0 and new[y][x-1] != "#" and new[y][x-1] != "O":
                        new[y] = new[y][:x-1] + "O" + new[y][x:]
                        new[y] = new[y][:x] + "." + new[y][x+1:]
                    elif turns[turn]=="S" and y < len(new)-1 and new[y+1][x] != "#" and new[y+1][x] != "O":
                        new[y+1] = new[y+1][:x] + "O" + new[y+1][x+1:]
                        new[y] = new[y][:x] + "." + new[y][x+1:]
                    elif turns[turn]=="E" and x < len(new[0])-1 and new[y][x+1] != "#" and new[y][x+1] != "O":
                        new[y] = new[y][:x+1] + "O" + new[y][x+2:]
                        new[y] = new[y][:x] + "." + new[y][x+1:]

                if new == prev:
                    if turn == len(turns)-1:
                        cycle += 1
                        all_cycles.append(new)
                        h = "".join(new)
                        if h in cycles:
                            print("FOUND !!")
                            print(f"Cycle found at {cycle} which was same as {cycles[h]}")

                            j = cycles[h]
                            cycle_len = cycle - cycles[h]
                            print(f"Cycle len = {cycle_len}")

                            score = 0
                            value_at_1000000000 = all_cycles[(1000000000 - j) % cycle_len + j - 1]
                            for i, line in enumerate(value_at_1000000000):
                                score += line.count("O") * (len(value_at_1000000000) - i)
                            return score
                        else:
                            cycles[h] = cycle
                    turn = (turn + 1) % len(turns)
                    break
                prev = new

        score = 0
        if part == 1:
            for i, line in enumerate(prev):
                score += line.count("O") * (len(prev) - i)
                print(line)

        return score


if __name__ == '__main__':

    level = 1
    expectedSampleResult = 136
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
