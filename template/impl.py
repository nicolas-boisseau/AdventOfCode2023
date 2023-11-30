import itertools
import os.path
#from py_linq import Enumerable

from common.common import DownloadIfNotExists, DetectCurrentDay

try:
    day = DetectCurrentDay()
    if day != 0:
        DownloadIfNotExists(f"https://adventofcode.com/2022/day/{day}/input")
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
    process(1, "sample.txt")
