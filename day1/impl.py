import itertools
import os.path
#from py_linq import Enumerable

from common.common import DownloadIfNotExists, DetectCurrentDay, PostAnswer

try:
    day = DetectCurrentDay()
    if day != 0:
        DownloadIfNotExists(f"https://adventofcode.com/2023/day/{day}/input")
except:
    pass

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")
    with open(filename) as f:
        lines = [l.replace("\n", "") for l in f.readlines()]

        # TODO

    return 0

if __name__ == '__main__':
    if process(1, "sample.txt") == 7:
        print("Part 1 sample OK")

        result = process(1, "input.txt")

        day = DetectCurrentDay()
        if day != 0:
            PostAnswer(f"https://adventofcode.com/2023/day/{day}/answer", result)
            print("Part 1 result posted !")

