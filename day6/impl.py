import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_score = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        times_input = lines[0]
        distances_input = lines[1]
        if part == 2:
            times_input = times_input.replace(" ", "")
            distances_input = distances_input.replace(" ", "")

        times = [int(t) for t in capture_all(r"(\d+)", times_input)]
        distances = [int(d) for d in capture_all(r"(\d+)", distances_input)]

        scores_by_index = defaultdict(int)
        for i, t in enumerate(times):
            best_distance = distances[i]
            for ms in range(0, t):
                if ((t - ms) * ms) > best_distance:
                    scores_by_index[i] += 1

        for s in scores_by_index.values():
            if total_score == 0:
                total_score = s
            else:
                total_score *= s
        return total_score


if __name__ == '__main__':

    level = 1
    expectedSampleResult = 288
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
