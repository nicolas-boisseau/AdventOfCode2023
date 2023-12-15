import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)

def custom_hash(s):
    current_value = 0
    for i, c in enumerate(s):
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    score = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        if part == 1:
            for s in lines[0].split(","):
                score += custom_hash(s)

            return score
        else:
            boxes = {}
            instructions = lines[0].split(",")
            for instr_raw in instructions:
                instr = capture(r"([a-z]+)([-=]+)([0-9]*)", instr_raw)
                print(f"current instr: {instr}")
                if len(instr) == 3:
                    box_id = custom_hash(instr[0])
                    op = instr[1]
                    label = 0 if instr[2] == "" else int(instr[2])
                    if box_id not in boxes:
                        boxes[box_id] = []
                    if op == "=":
                        if len([v for v in boxes[box_id] if v[0] == instr[0]]) == 0:
                            boxes[box_id].append((instr[0], label))
                        else:
                            for i, v in enumerate(boxes[box_id]):
                                if v[0] == instr[0]:
                                    boxes[box_id][i] = (instr[0], label)
                    else: # remove
                        for i in boxes.keys():
                            boxes[i] = [x for x in boxes[i] if x[0] != instr[0]]
                for k in boxes.keys():
                    print(f"Box {k} : {boxes[k]}")
                print()

            # compute score
            score = 0
            for k in boxes.keys():
                for i, v in enumerate(boxes[k]):
                    score += (custom_hash(v[0])+1) * (i+1) * v[1]
            return score

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 145
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
