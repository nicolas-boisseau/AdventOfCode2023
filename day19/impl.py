import os.path

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
    is_workflow = True
    for line in lines:
        if line == "":
            is_workflow = False
            continue
        if is_workflow:
            values = capture(r"([a-z]+)\{([a-zA-Z0-9<>=:,]+)\}", line)
            name = values[0]
            steps_raw = values[1].split(",")
            steps = []
            for i in range(len(steps_raw)):
                step_raw = steps_raw[i].split(":")
                if len(step_raw) == 1:
                    step = ("direct_output", step_raw[0])
                else:
                    step_op = step_raw[0]
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
    return workflows, parts

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

    for part in parts[0:1]:
        current_workflow_name = "in"
        while current_workflow_name not in ["A", "R"]:
            current_workflow = [w for w in workflows if w[0] == current_workflow_name][0]
            current_workflow_name = execute_workflow(current_workflow, part)
            print(current_workflow_name)



    return 0

def part2(lines):
    return 4


if __name__ == '__main__':

    part = 1
    expectedSampleResult = -1

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
