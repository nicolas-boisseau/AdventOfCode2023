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
            for i in range(0, len(pattern)):
                j = i
                max_reflect_horizontal = 0
                reflect = 1
                while 0 < j-reflect < len(pattern) - 1 and 0 < j+reflect < len(pattern) - 1:
                    prev_line = pattern[j-reflect+1]
                    next_line = pattern[j+reflect]
                    if prev_line == next_line:
                        reflect += 1
                        if reflect > max_reflect_horizontal:
                            max_reflect_horizontal = reflect
                    else:
                        break
                horizontal_reflects.append((i, max_reflect_horizontal))
            for i in range(0, len(pattern[0])):
                j = i
                max_reflect_vertical = 0
                reflect = 1
                while 0 < j-reflect < len(pattern) - 1 and 0 < j+reflect < len(pattern) - 1:
                    prev_col = [pattern[k][j-reflect+1] for k in range(0, len(pattern))]
                    next_col = [pattern[k][j+reflect] for k in range(0, len(pattern))]
                    if prev_col == next_col:
                        reflect += 1
                        if reflect > max_reflect_vertical:
                            max_reflect_vertical = reflect
                    else:
                        break
                vertical_reflects.append((i, max_reflect_vertical))

            best_vertical_pos = Enumerable(vertical_reflects).order_by_descending(lambda x: x[1]).select(lambda x: x[0]).first()
            best_horizontal_pos = Enumerable(horizontal_reflects).order_by_descending(lambda x: x[1]).select(lambda x: x[0]).first()

            total_part_1 += best_vertical_pos * 100
            total_part_1 += best_horizontal_pos

        return total_part_1






if __name__ == '__main__':

    level = 1
    expectedSampleResult = -1
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
