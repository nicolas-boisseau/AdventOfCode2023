import itertools
import os.path

from py_linq import Enumerable

#from py_linq import Enumerable

from common.common import DownloadInputIfNotExists, PostAnswer

DownloadInputIfNotExists(2023)

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total = 0
    with open(filename) as f:
        lines = [l.replace("\n", "") for l in f.readlines()]

        for line in lines:

            if part == 2:
                line = replaceNumbers(line)

            letters = Enumerable([l for l in line])
            digits = letters.where(lambda l: l.isdigit())
            #print(digits)

            number = int(digits.to_list()[0] + digits.to_list()[-1])
            #print(number)
            total += number


    return total

def replaceNumbers(line):
    newLineSoFar = ""
    for l in line:
        newLineSoFar += l
        newLineSoFar = replaceNumberRaw(newLineSoFar)
    return newLineSoFar

def replaceNumberRaw(line):
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

        PostAnswer(2023, level, result)
        print(f"Part {level} result posted !")

