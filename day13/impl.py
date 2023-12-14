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

def reflections(pattern):
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
    return reflections

def mutations(pattern):
    for y in range(0, len(pattern)):
        for x in range(0, len(pattern[0])):
            mutant = pattern.copy()
            #mutant[y][x] = "#" if mutant[y][x] == "." else "."
            mutant[y] = mutant[y][:x] + ("#" if mutant[y][x] == "." else ".") + mutant[y][x+1:]
            yield mutant


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        patterns = read_patterns(lines)

        horizontal_reflects = []
        vertical_reflects = []
        initial_reflects = {}
        for i, pattern in enumerate(patterns):
            r = reflections(pattern)
            #print(r)
            if r[0][0] == "h":
                horizontal_reflects.append(r[0][1])
            else:
                vertical_reflects.append(r[0][1])
            initial_reflects[i] = r[0]

        if part == 2:
            horizontal_reflects = []
            vertical_reflects = []
            for i, pattern in enumerate(patterns):
                for mutant in mutations(pattern):
                    r = reflections(mutant)
                    if len(r) == 0 or (len(r) == 1 and r[0] == initial_reflects[i]):
                        continue

                    print(f"new reflects = {len(r)}")
                    print(f"initial reflects = {initial_reflects[i]}")
                    print(f"new reflects = {r}")
                    r = [rr for rr in r if rr != initial_reflects[i]]
                    print(f"to keep reflects = {r}")
                    print()

                    #print(r)
                    if r[0][0] == "h":
                        horizontal_reflects.append(r[0][1])
                    else:
                        vertical_reflects.append(r[0][1])

                    break

            total += sum(horizontal_reflects) * 100
            total += sum(vertical_reflects)

            return total

        else:
            total += sum(horizontal_reflects) * 100
            total += sum(vertical_reflects)

            return total






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
