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

def rows_before(pattern, index, reductor=0):
    return pattern[reductor:index]

def rows_after(pattern, index, reductor=0):
    return pattern[index:len(pattern)-reductor]

def cols_before(pattern, index, reductor=0):
    cols = []
    for i in range(reductor, index):
        cols.append("".join([c[i] for c in pattern]))
    return cols

def cols_after(pattern, index, reductor=0):
    cols_right = []
    for i in range(index, len(pattern[0])-reductor):
        cols_right.append("".join([c[i] for c in pattern]))
    return cols_right

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

            reflections = []

            for i in range(0, len(pattern[0])):
                before = reversed(cols_before(pattern, i))
                after = cols_after(pattern, i)
                j = 0
                while j < len(before) and j < len(after) and before[j] == after[j]:
                    j += 1
                if j > 0 and (j == len(before) or j == len(after)):
                    reflections.append(("v", i, j))
                    break


            for i in range(0, len(pattern)):
                before = reversed(rows_before(pattern, i))
                after = rows_after(pattern, i)
                j = 0
                while j < len(before) and j < len(after) and before[j] == after[j]:
                    j += 1
                if j > 0 and (j == len(before) or j == len(after)):
                    reflections.append(("h", i, j))
                    break


            print(reflections)

            max = Enumerable(reflections).order_by_descending(lambda x: x[2]).first()

            if max[0] == "h":
                horizontal_reflects.append(max[1])
            else:
                vertical_reflects.append(max[1])

            print(horizontal_reflects)
            print(vertical_reflects)

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
