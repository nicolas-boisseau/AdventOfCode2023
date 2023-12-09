import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all

download_input_if_not_exists(2023)

class Suit:
    def __init__(self, initial_sequence):
        self.initial_sequence = initial_sequence
        self.all_sequences = []
        self.all_sequences.append(initial_sequence)

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

        suits = []
        for line in lines:
            suit = [int(n) for n in capture_all(r"([0-9-]+)", line)]
            suits.append(Suit(suit))

        while not Enumerable(suits).all(lambda s: s.is_last_sequence()):
            for suit in suits:
                if not suit.is_last_sequence():
                    suit.compute_next_diff()

        total = 0
        if part == 1:
            for suit in suits:
                nextValue = suit.compute_next_value()
                total += nextValue
        else:
            for suit in suits:
                nextValue = suit.compute_previous_value()
                total += nextValue

        return total


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
