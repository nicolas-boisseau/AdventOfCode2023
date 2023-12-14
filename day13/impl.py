import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def read_patterns(lines):
    patterns = []
    cur_pattern = []
    for line in lines:
        if line == "":
            patterns.append(cur_pattern)
            cur_pattern = []
            continue
        cur_pattern.append(line)
    patterns.append(cur_pattern)
    return patterns

def reversed(list):
    list.reverse()
    return list

def rotate_90(pattern):
    rotated_pattern = []
    for j in range(len(pattern[0])):
        current = ""
        for i in range(len(pattern)):
            current += pattern[i][j]
        rotated_pattern.append(current)
    return rotated_pattern

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part_1 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        patterns = read_patterns(lines)

        horizontal_reflects = []
        vertical_reflects = []
        for pattern in patterns:


            middle = len(pattern)//2 + 1

            if reversed(pattern[0:middle-1]) == pattern[middle-1:len(pattern)-1]:
                horizontal_reflects.append(middle-1)
            elif reversed(pattern[1:middle]) == pattern[middle:]:
                horizontal_reflects.append(middle)

            middle_v = len(pattern[0])//2 + 1

            # rotate pattern
            middle = len(pattern[0]) // 2 + 1

            cols_left = []
            for i in range(0, middle-1):
                cols_left.append("".join([c[i] for c in pattern]))
            cols_right = []
            for i in range(middle-1, len(pattern[0])-1):
                cols_right.append("".join([c[i] for c in pattern]))


            if reversed(cols_left) == cols_right:
                vertical_reflects.append(middle-1)
            else:
                cols_left = []
                for i in range(1, middle):
                    cols_left.append("".join([c[i] for c in pattern]))
                cols_right = []
                for i in range(middle, len(pattern[0])):
                    cols_right.append("".join([c[i] for c in pattern]))

                if reversed(cols_left) == cols_right:
                    vertical_reflects.append(middle)





            print(f"h: {horizontal_reflects}")
            print(f"v: {vertical_reflects}")

            print()

        total_part_1 += sum(horizontal_reflects) * 100
        total_part_1 += sum(vertical_reflects)

        return total_part_1






if __name__ == '__main__':

    level = 1
    expectedSampleResult = 405
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
