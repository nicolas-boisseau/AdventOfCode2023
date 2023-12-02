import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer

download_input_if_not_exists(2023)


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        for line in lines:

            if part == 2:
                line = replace_numbers(line)

            letters = Enumerable([letter for letter in line])
            digits = letters.where(lambda char: char.isdigit())
            # print(digits)

            number = int(digits.to_list()[0] + digits.to_list()[-1])
            # print(number)
            total += number

    return total


def replace_numbers(line):
    new_line_so_far = ""
    for char in line:
        new_line_so_far += char
        new_line_so_far = replace_number_raw(new_line_so_far)
    return new_line_so_far


def replace_number_raw(line):
    line = line.replace("one", "1")
    line = line.replace("two", "2")
    line = line.replace("three", "3")
    line = line.replace("four", "4")
    line = line.replace("five", "5")
    line = line.replace("six", "6")
    line = line.replace("seven", "7")
    line = line.replace("eight", "8")
    line = line.replace("nine", "9")
    # line = line.replace("zero", "0")
    return line


if __name__ == '__main__':

    level = 2
    expectedSampleResult = 281
    sampleFile = "sample2.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
