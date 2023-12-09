import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)

class NumSequence:
    def __init__(self, initial_sequence):
        self.initial_sequence = initial_sequence
        self.all_sequences = []
        self.all_sequences.append(initial_sequence)

    def compute_all_diffs(self):
        while not self.is_last_sequence():
            self.compute_next_diff()

    def compute_next_diff(self):
        if self.is_last_sequence():
            return
        current_sequence = self.all_sequences[-1]
        #print(f"initial = {self.initial_sequence}")
        new_sequence = []
        for i in range(1, len(current_sequence), 1):
            new_sequence.append(current_sequence[i] - current_sequence[i-1])
        self.all_sequences.append(new_sequence)
        #print(new_sequence)

    def is_last_sequence(self):
        return Enumerable(self.all_sequences[-1]).all(lambda n: n == 0)

    def compute_next_value(self):
        if not self.is_last_sequence():
            print("should compute diffs first !")
            return
        for i in range(len(self.all_sequences) - 2, -1, -1):
            self.all_sequences[i].append(self.all_sequences[i][-1] + self.all_sequences[i+1][-1])
        return self.all_sequences[0][-1]

    def compute_previous_value(self):
        if not self.is_last_sequence():
            print("should compute diffs first !")
            return
        for i in range(len(self.all_sequences) - 2, -1, -1):
            self.all_sequences[i].insert(0, self.all_sequences[i][0] - self.all_sequences[i+1][0])
        return self.all_sequences[0][0]


def process(part, filename):
    if not (os.path.exists(filename)):
        print("Input file not found !")

    print("Input file OK ! Starting processing...")

    with open(filename) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        sequences = []
        for line in lines:
            s = [int(n) for n in capture_all(r"([0-9-]+)", line)]
            new_sequence = NumSequence(s)
            new_sequence.compute_all_diffs()
            sequences.append(new_sequence)

        if part == 1:
            return sum([s.compute_next_value() for s in sequences])
        else:
            return sum([s.compute_previous_value() for s in sequences])


if __name__ == '__main__':

    level = 2
    expectedSampleResult = 2
    sampleFile = "sample.txt"

    if process(level, sampleFile) == expectedSampleResult:
        print(f"Part {level} sample OK")

        result = process(level, "input.txt")
        print(f"Part {level} result is {result}")

        post_answer(2023, level, result)
        print(f"Part {level} result posted !")
