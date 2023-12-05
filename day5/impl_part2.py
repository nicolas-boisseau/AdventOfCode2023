import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)


class MapperRule:
    def __init__(self, destination_start, source_start, range):
        self.range = range
        self.source_start = source_start
        self.destination_start = destination_start

    def map(self, sourceNumber):
        if sourceNumber < self.source_start or sourceNumber >= self.source_start + self.range:
            return -1
        return self.destination_start + (sourceNumber - self.source_start)

    def reverse_map(self, destination_number):
        if destination_number < self.destination_start or destination_number >= self.destination_start + self.range:
            return -1
        return self.source_start + (destination_number - self.destination_start)

    def __str__(self):
        return str(self.map)

class Mapper:
    def __init__(self, source_name, destination_name):
        self.source_name = source_name
        self.destination_name = destination_name
        self.rules = []

    def add_rule(self, destination_start, source_start, range):
        self.rules.append(MapperRule(destination_start, source_start, range))

    def map(self, sourceNumber):
        for rule in self.rules:
            mapped = rule.map(sourceNumber)
            if mapped != -1:
                return mapped
        return sourceNumber

    def reverse_map(self, destination_number):
        for rule in self.rules:
            mapped = rule.reverse_map(destination_number)
            if mapped != -1:
                return mapped
        return destination_number

    def __str__(self):
        return str(self.map)

class Pipeline:
    def __init__(self):
        self.mappers = []

    def add_mapper(self, mapper):
        self.mappers.append(mapper)

    def map(self, sourceNumber):
        for mapper in self.mappers:
            sourceNumber = mapper.map(sourceNumber)
        return sourceNumber

    def __str__(self):
        return str(self.map)

    def reverse_map(self, destination_number):
        for mapper in reversed(self.mappers):
            destination_number = mapper.reverse_map(destination_number)
        return destination_number

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        seeds = []
        seeds_ranges = []
        seedsRaw = capture_all(r"(\d+)", lines[0].split(": ")[1])
        if part == 1:
            seeds = [int(n) for n in seedsRaw]
        else:
            seed_pairs = [int(n) for n in seedsRaw]
            for i in range(0, len(seed_pairs), 2):
                seeds_ranges.append({"start": seed_pairs[i], "end": seed_pairs[i] + seed_pairs[i+1] })

        pipeline = Pipeline()
        current_mapper = None

        for line in lines[2:]:
            if "to" in line:
                pipelineRaw = capture(r"([a-z]+)-to-([a-z]+) map:", line)
                source_name = pipelineRaw[0]
                destination_name = pipelineRaw[1]
                current_mapper = Mapper(source_name, destination_name)
            elif line == "":
                pipeline.add_mapper(current_mapper)
            else:
                rule = capture(r"(\d+) (\d+) (\d+)", line)
                current_mapper.add_rule(int(rule[0]), int(rule[1]), int(rule[2]))

        if part == 1:
            converted = []
            for seed in seeds:
                converted.append(pipeline.map(seed))

            #converted = [pipeline.map(seed) for seed in seeds]

            return min(converted)
        else:
            for i in range(26000000, 26829170, 1):
                test = pipeline.reverse_map(i)
                if isInRange(test, seeds_ranges):
                    return i

def isInRange(number, ranges):
    for range in ranges:
        if range["start"] <= number < range["end"]:
            return True
    return False

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 46
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        if result is not None:
            post_answer(2023, level, result)
            print(f"Part {level} result posted !")
        else:
            print("Result is None...")