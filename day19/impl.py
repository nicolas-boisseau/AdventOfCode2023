import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)


def step_func(x, x_value, step_op_part, step_op_op, step_op_value, output):
    if step_op_op == "<" and x == step_op_part and x_value < step_op_value:
        return output
    elif step_op_op == ">" and x == step_op_part and x_value > step_op_value:
        return output
    else:
        return None

def interpret_input(lines):
    workflows = []
    parts = []
    g = defaultdict(list)
    is_workflow = True
    for line in lines:
        if line == "":
            is_workflow = False
            continue
        if is_workflow:
            values = capture(r"([a-z]+)\{([a-zA-Z0-9<>=:,]+)\}", line)
            name = values[0]
            g[name] = []
            steps_raw = values[1].split(",")
            steps = []
            for i in range(len(steps_raw)):
                step_raw = steps_raw[i].split(":")
                if len(step_raw) == 1:
                    step = ("direct_output", step_raw[0])
                    g[name].append(("1=1", step_raw[0]))
                else:
                    step_op = step_raw[0]
                    g[name].append((step_op, step_raw[1]))
                    step_op_values = capture(r"([a-z]+)([<>])([0-9]+)", step_op)
                    step_op_part = step_op_values[0]
                    step_op_op = step_op_values[1]
                    step_op_value = int(step_op_values[2])
                    step = ("stepfunc", step_op_part, step_op_op, step_op_value, step_raw[1])

                steps.append(step)
            workflows.append((name, steps))
        else:
            all_values = capture_all(r"([a-z]+)=([0-9]+)", line)
            part = []
            for values in all_values:
                part.append((values[0], int(values[1])))
            parts.append(part)
    return workflows, parts, g

def execute_workflow(workflow, part):
    for step in workflow[1]:
        for p in part:
            if step[0] == "direct_output":
                computed = step[1]
            else:
                computed = step_func(p[0], p[1], step[1], step[2], step[3], step[4])
            if computed is not None:
                return computed


def part1(lines):
    workflows, parts = interpret_input(lines)
    print(workflows)
    print(parts)

    total = 0
    for part in parts:
        current_workflow_name = "in"
        while current_workflow_name not in ["A", "R"]:
            current_workflow = [w for w in workflows if w[0] == current_workflow_name][0]
            current_workflow_name = execute_workflow(current_workflow, part)
            print(current_workflow_name)
        if current_workflow_name == "A":
            total += sum(p[1] for p in part)
    return total


def getAllPaths(g, current, end, visited, path, all_paths):
    # Mark the current node as visited and store in path
    visited[current] = True
    path.append(current)

    # If current vertex is same as destination, then print
    # current path[]
    if current == end:
        all_paths.append(path.copy())
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for (op, i) in g[current]:
            if i not in visited or not visited[i]:
                getAllPaths(g, i, end, visited, path, all_paths)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[current] = False

    return all_paths

def part2(lines):
    workflows, parts, g = interpret_input(lines)
    print(workflows)
    print(parts)
    print(g)
    print()

    all_paths = getAllPaths(g, "in", "A", defaultdict(bool), [], [])
    print(all_paths)



    ops_by_path = defaultdict(list)
    for i, path in enumerate(all_paths): # try 1st
        for j, step in enumerate(path):
            if step == "A":
                break
            op = [op for (op, next) in g[step] if next == path[j+1]][0]
            ops_by_path[i].append(op)

    print(ops_by_path)

    bounds_by_path = defaultdict(dict)
    for i in ops_by_path.keys():
        ops = ops_by_path[i]
        bounds_by_path[i] = {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        }
        for op in ops:
            if op == "1=1":
                continue
            op_values = capture(r"([a-z]+)([<>])([0-9]+)", op)
            op_part = op_values[0]
            op_op = op_values[1]
            op_value = int(op_values[2])
            if op_op == "<":
                if op_value < bounds_by_path[i][op_part][1]:
                    bounds_by_path[i][op_part] = (bounds_by_path[i][op_part][0], op_value)
            else:
                if op_value > bounds_by_path[i][op_part][0]:
                    bounds_by_path[i][op_part] = (op_value, bounds_by_path[i][op_part][1])

        print(f"bounds_by_path[{i}]= {bounds_by_path[i]}")
    print()
    # merge common bounds in bounds_by_path[i]
    for i in bounds_by_path.keys():
        for j in bounds_by_path.keys():
            if i == j:
                continue
            for op in bounds_by_path[i].keys():
                if op not in bounds_by_path[j]:
                    continue
                if bounds_by_path[i][op][0] > bounds_by_path[j][op][0]:
                    bounds_by_path[i][op] = (bounds_by_path[i][op][0], bounds_by_path[j][op][1])
                if bounds_by_path[i][op][1] < bounds_by_path[j][op][1]:
                    bounds_by_path[i][op] = (bounds_by_path[j][op][0], bounds_by_path[i][op][1])



    print(bounds_by_path)

    total = 0
    for i in bounds_by_path.keys():
        sub_total = 1
        for op in bounds_by_path[i].keys():
            sub_total *= bounds_by_path[i][op][1] - bounds_by_path[i][op][0] + 1
        total += sub_total
    return total

def is_contained_in_bounds(bounds, values):
    if values[]

if __name__ == '__main__':

    part = 1
    expectedSampleResult = 19114

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
