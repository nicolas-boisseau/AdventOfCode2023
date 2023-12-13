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

        for pattern in patterns:
            horizontal_reflects = []
            vertical_reflects = []

            middle = len(pattern)//2 + 1

            rev = pattern[0:middle]
            rev.reverse()
            if "".join(rev) == "".join(pattern[middle:]):
                print(middle)
            else:
                rev = pattern[0:middle-1]
                rev.reverse()
                if "".join(pattern[0:middle-1]) == "".join(pattern[middle-1:len(pattern)-2]):
                    print(middle-1)
                else:
                    rev = pattern[0:middle - 1]
                    rev.reverse()
                    if "".join(pattern[1:middle+1]) == "".join(pattern[middle+1:]):
                        print(middle+1)

            # for i in range(0, len(pattern[0])):
            #     max_reflect_vertical = 0
            #     reflect = 1
            #     is_reflect = False
            #     while 0 < i-reflect+1 < len(pattern) - 1 and 0 < i+reflect < len(pattern) - 1:
            #         prev_col = [pattern[k][i-reflect+1] for k in range(0, len(pattern))]
            #         next_col = [pattern[k][i+reflect] for k in range(0, len(pattern))]
            #         if prev_col == next_col:
            #             reflect += 1
            #             is_reflect = True
            #         else:
            #             break
            #     if is_reflect and reflect >= len(pattern[0])//2:
            #         vertical_reflects.append(i)
            #
            # for i in range(0, len(pattern)):
            #     max_reflect_horizontal = 0
            #     reflect = 1
            #     is_reflect = False
            #     while 0 < i-reflect+1 < len(pattern) - 1 and 0 < i+reflect < len(pattern) - 1:
            #         prev_line = pattern[i-reflect+1]
            #         next_line = pattern[i+reflect]
            #         if prev_line == next_line:
            #             reflect += 1
            #             is_reflect = True
            #         else:
            #             break
            #     if is_reflect and reflect >= len(pattern)//2:
            #         horizontal_reflects.append(i)



            print(horizontal_reflects)
            print(vertical_reflects)

            # total_part_1 += best_vertical_pos * 100
            # total_part_1 += best_horizontal_pos

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
