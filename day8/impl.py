import os.path
from collections import defaultdict

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        instructions = lines[0]

        phases = {}
        i = 0
        for line in lines[2:]:
            nodes = capture_all(r"([0-9A-Z]{3})", line)
            phases[nodes[0]] = (nodes[1], nodes[2])

        if part == 1:
            currentNodeName = "AAA"
            i = 0
            total_steps = 0
            while currentNodeName != "ZZZ":
                next_instruction = instructions[i]
                if next_instruction == "R":
                    currentNodeName = phases[currentNodeName][1]
                else:
                    currentNodeName = phases[currentNodeName][0]
                i = (i + 1) % len(instructions)
                total_steps += 1

            return total_steps
        else:
            current_nodes = Enumerable(phases.keys()).where(lambda k: k.endswith("A")).select(lambda k: k).to_list()
            print(current_nodes)

            tracking = {}
            for n in current_nodes:
                tracking[n] = {
                    "starting_node": n,
                    "current_node": n,
                    "z_pos": []
                }

            total_steps = 0
            i = 0
            while not Enumerable(tracking.keys()).all(lambda k: tracking[k]["current_node"].endswith("Z")) and total_steps < 100000:
                total_steps += 1
                next_instruction = instructions[i]
                if next_instruction == "R":
                    for j, node in enumerate(tracking.keys()):
                        tracking[node]["current_node"] = phases[tracking[node]["current_node"]][1]
                        if tracking[node]["current_node"].endswith("Z"):
                            tracking[node]["z_pos"].append(total_steps)
                            #print(f"for node {j} a Z node has been found : {current_nodes[j]} at step {total_steps}")
                else:
                    for j, node in enumerate(tracking.keys()):
                        tracking[node]["current_node"] = phases[tracking[node]["current_node"]][0]
                        if tracking[node]["current_node"].endswith("Z"):
                            tracking[node]["z_pos"].append(total_steps)
                            #print(f"for node {j} a Z node has been found : {current_nodes[j]} at step {total_steps}")
                i = (i + 1) % len(instructions)

            print(tracking)

            patterns = [tracking[node]["z_pos"][1] - tracking[node]["z_pos"][0] for node in tracking.keys() if len(tracking[node]["z_pos"]) >= 2]

            result = compute_lcm(patterns[0], patterns[1])
            for i in range(2, len(patterns)):
                result = compute_lcm(result, patterns[i])

            return result

def compute_lcm(a, b):

   return a / gcd(a,b) * b

def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 6
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
