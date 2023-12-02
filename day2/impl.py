import itertools
import os.path

from py_linq import Enumerable

#from py_linq import Enumerable

from common.common import DownloadInputIfNotExists, PostAnswer, Capture, CaptureAll

DownloadInputIfNotExists(2023)

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [l.replace("\n", "") for l in f.readlines()]

        for line in lines:
            game = line.split(":")
            gameId = int(Capture(r"Game (\d+)", game[0])[0])
            print(f"Game {gameId}")

            plays = game[1].split(";")
            part1_KO = False
            minCubeCounts = {"red": 0, "blue": 0, "green": 0}
            for play in plays:
                cubesCounts = {"red": 0, "blue": 0, "green": 0}

                jets = CaptureAll(r"(\d+) (red|blue|green)", play)
                if len(jets) == 0:
                    continue

                if part == 1:
                    for jet in jets:
                        cubesCounts[jet[1]] += int(jet[0])

                    if cubesCounts["red"] > 12 or cubesCounts["blue"] > 14 or cubesCounts["green"] > 13:
                        print(f"Game {gameId} is invalid !")
                        part1_KO = True
                else:
                    for jet in jets:
                        if int(jet[0]) > minCubeCounts[jet[1]]:
                            minCubeCounts[jet[1]] = int(jet[0])

            if not part1_KO:
                total_part1 += gameId

            total_part2 += minCubeCounts["red"] * minCubeCounts["blue"] * minCubeCounts["green"]

        if part == 1:
            return total_part1
        else:
            return total_part2

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 2286
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        PostAnswer(2023, level, result)
        print(f"Part {level} result posted !")

