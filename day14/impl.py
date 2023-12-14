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
        print(line)

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
        if part == 2:
            turns = ["N", "W", "S", "E"]
        turn = 0
        for i in range(len(turns)*1):
            while True:
                new = prev.copy()
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
                    turn = (turn + 1) % len(turns)
                    break
                balls = get_balls_positions(new)
                prev = new
                print_lines(new)
                print()

        score = 0
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
