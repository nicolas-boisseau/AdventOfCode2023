import os.path
from collections import defaultdict

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

def interpret_input(lines):
    modules = defaultdict(tuple)
    for i, line in enumerate(lines):
        parts = line.split(" -> ")
        module_type = "broadcaster" if parts[0][0] == "b" else ("Flip-flop" if parts[0][0] == "%" else "Conjunction")
        module_name = parts[0].replace("%","").replace("&", "")
        if module_type == "broadcaster":
            modules[module_name] = (module_type, parts[1].split(", "))
        elif module_type == "Flip-flop":
            state = "off"
            modules[module_name] = (module_type, parts[1].split(", "), state)
        else:
            memory = defaultdict(bool)
            modules[module_name] = (module_type, parts[1].split(", "), memory)

    # init Conjuntion memory
    for module_name, module in modules.items():
        if module[0] == "Conjunction":
            for other_module_name, other_module in modules.items():
                if any([other_next for other_next in other_module[1] if other_next == module_name]):
                    module[2][other_module_name] = False

    return modules

pulses = {
    "low": 0,
    "high": 0
}
button_pressed_count = 0

def send_pulse(pulse_type, current_module_name, modules, previous_module_name=None):
    stack = [(pulse_type, current_module_name, previous_module_name)]
    while stack:
        pulse_type, current_module_name, previous_module_name = stack.pop(0)
        #print(f"{previous_module_name} -{pulse_type}-> {current_module_name}")
        global pulses, button_pressed_count
        pulses[pulse_type] += 1
        if len(modules[current_module_name]) == 0:
            if current_module_name == "rx" and pulse_type == "low":
                print("rx received a low pulse !")
                print(button_pressed_count)
                return button_pressed_count
            continue
        current_module_type = modules[current_module_name][0]
        nexts = modules[current_module_name][1]
        if current_module_type == "broadcaster":
            for next_module in nexts:
                stack.append((pulse_type, next_module, current_module_name))
        elif current_module_type == "Flip-flop":
            prev_state = modules[current_module_name][2]
            new_state = "off" if prev_state == "on" else "on"
            if pulse_type == "low":
                modules[current_module_name] = (
                modules[current_module_name][0], modules[current_module_name][1], new_state)

            for next_module in nexts:
                if pulse_type == "low":
                    if prev_state == "on":
                        stack.append(("low", next_module, current_module_name))
                    else:
                        stack.append(("high", next_module, current_module_name))
        elif current_module_type == "Conjunction":
            memory = modules[current_module_name][2]
            memory[previous_module_name] = pulse_type == "high"
            modules[current_module_name] = (modules[current_module_name][0], modules[current_module_name][1], memory)
            for next_module in nexts:
                if all(memory.values()):
                    stack.append(("low", next_module, current_module_name))
                else:
                    stack.append(("high", next_module, current_module_name))
        else:
            print(current_module_type)
            #raise Exception("Unknown module type")




def push_button(modules):
    global button_pressed_count
    button_pressed_count += 1
    send_pulse("low", "broadcaster", modules, "button")


def part1(lines):

    modules = interpret_input(lines)
    print(modules)

    for i in range(1000):
        push_button(modules)

    return pulses["high"] * pulses["low"]

def part2(lines):
    global button_pressed_count
    modules = interpret_input(lines)
    print(modules)

    for i in range(100000000):
        rx = push_button(modules)
        if rx is not None:
            print("rx received a low pulse !")
            return button_pressed_count

    return 0

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
