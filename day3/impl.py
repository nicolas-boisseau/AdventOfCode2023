import os.path

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        m = extract_matrix(lines)

        current_number = ""
        current_symbol = {"symbol": "", "symbol_position": ""}
        is_near_symbol = False

        previous_was_number = False
        gear_count_by_position = {}
        for y, y_value in enumerate(m):
            for x, x_value in enumerate(m[y]):
                if m[y][x].isdigit():
                    current_number += m[y][x]
                    is_near_symbol, symbol, symbol_position = check_is_near_symbol(is_near_symbol, m, x, y)
                    if is_near_symbol and symbol != "" and symbol != ".":
                        current_symbol = {"symbol": symbol, "symbol_position": symbol_position}
                    previous_was_number = True

                if not m[y][x].isdigit() and previous_was_number:
                    if is_near_symbol:
                        symbol = current_symbol["symbol"]
                        symbol_position = current_symbol["symbol_position"]
                        total_part1 += int(current_number)
                        if symbol == "*":
                            if gear_count_by_position.get(symbol_position) is None:
                                gear_count_by_position[symbol_position] = {"count":0, "score":0}
                            if gear_count_by_position[symbol_position]["count"] >= 1:
                                gear_count_by_position[symbol_position]["score"] *= int(current_number)
                            else:
                                gear_count_by_position[symbol_position]["score"] += int(current_number)
                            gear_count_by_position[symbol_position]["count"] += 1

                    current_number = ""
                    is_near_symbol = False
                    previous_was_number = False

        for gear_count in gear_count_by_position.values():
            if gear_count["count"] == 2:
                total_part2 += gear_count["score"]

        if part == 1:
            return total_part1
        else:
            return total_part2


def check_is_near_symbol(is_near_symbol, m, x, y):
    symbol = ""
    symbol_position = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + j < 0 or x + j >= len(m[y]) or y + i < 0 or y + i >= len(m):
                continue
            if not m[y + i][x + j].isdigit() and m[y + i][x + j] != ".":
                is_near_symbol = True
                symbol = m[y + i][x + j]
                symbol_position = f"{y + i}_{x + j}"
    return is_near_symbol, symbol, symbol_position


def extract_matrix(lines):
    m = create_matrix(len(lines), len(lines[0]))
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            m[y][x] = char
    return m


def create_matrix(h, w):
    return [[0 for x in range(w)] for y in range(h)]

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 467835
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
