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

def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    total_part1 = 0
    total_part2 = 0
    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        seeds = []
        seedsRaw = capture_all(r"(\d+)", lines[0].split(": ")[1])
        if part == 1:
            seeds = [int(n) for n in seedsRaw]
        else:
            for i in range(int(seedsRaw[0]), int(seedsRaw[1]) + int(seedsRaw[0])):
                seeds.append(i)
            for j in range(int(seedsRaw[2]), int(seedsRaw[3]) + int(seedsRaw[2])):
                seeds.append(j)

        pipeline = Pipeline()
        source_name = ""
        destination_name = ""
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

        converted = []
        for seed in seeds:
            converted.append(pipeline.map(seed))


        return min(converted)

if __name__ == '__main__':

    level = 2
    expectedSampleResult = 46
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
