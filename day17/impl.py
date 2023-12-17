import os.path

from py_linq import Enumerable

from common.common import download_input_if_not_exists, post_answer, capture, capture_all, read_input_lines

download_input_if_not_exists(2023)

directions = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}
new_directions = {
    "N": ("W", "E"),
    "E": ("N", "S"),
    "S": ("E", "W"),
    "W": ("S", "N"),
}

class Node:
    def __init__(self, y, x, dir, speed, heatloss, board, h, w, min_speed, max_speed):
        self.y = y
        self.x = x
        self.dir = dir
        self.board = board
        self.speed = speed
        self.heatloss = heatloss
        self.h = h
        self.w = w
        self.min_speed = min_speed
        self.max_speed = max_speed

    def forward(self):
        if self.speed < self.max_speed:
            new_y = self.y + directions[self.dir][0]
            new_x = self.x + directions[self.dir][1]
            if self.is_out_of_bounds(new_y, new_x):
                return []
            new_speed = self.speed + 1
            new_heatloss = self.heatloss + self.board[(new_y, new_x)]
            return [
                Node(new_y, new_x, self.dir, new_speed, new_heatloss, self.board, self.h, self.w, self.min_speed, self.max_speed),
            ]
        return []


    def left(self):
        if self.speed < self.min_speed:
            return []
        new_dir = new_directions[self.dir][0]
        new_y = self.y + directions[new_dir][0]
        new_x = self.x + directions[new_dir][1]
        if self.is_out_of_bounds(new_y, new_x):
            return []
        new_speed = 1
        new_heatloss = self.heatloss + self.board[(new_y, new_x)]
        return [
            Node(new_y, new_x, new_dir, new_speed, new_heatloss, self.board, self.h, self.w, self.min_speed, self.max_speed),
        ]
    def right(self):
        if self.speed < self.min_speed:
            return []
        new_dir = new_directions[self.dir][1]
        new_y = self.y + directions[new_dir][0]
        new_x = self.x + directions[new_dir][1]
        if self.is_out_of_bounds(new_y, new_x):
            return []
        new_speed = 1
        new_heatloss = self.heatloss + self.board[(new_y, new_x)]
        return [
            Node(new_y, new_x, new_dir, new_speed, new_heatloss, self.board, self.h, self.w, self.min_speed, self.max_speed),
        ]

    def is_out_of_bounds(self, y, x):
        return y < 0 or y >= self.h or x < 0 or x >= self.w

    def finished(self):
        return self.y == self.h - 1 and self.x == self.w - 1

    def __repr__(self):
        return f"Node({self.y}, {self.x}, {self.dir}, {self.speed}, {self.heatloss})"


def compute_heatloss(lines, min_speed, max_speed):
    height = len(lines)
    width = len(lines[0])
    board = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            board[(y, x)] = int(char)

    heatlosses = {
        (0, 0, "E", 1): 0,
        (0, 0, "S", 1): 0
    }
    nodes = [
        Node(0, 0, "E", 0, 0, board, height, width, min_speed, max_speed),
        Node(0, 0, "S", 0, 0, board, height, width, min_speed, max_speed),
    ]
    while nodes:

        next_nodes = []
        for n in nodes:
            possible_nexts = n.forward()
            possible_nexts += n.left()
            possible_nexts += n.right()

            for next in possible_nexts:
                new_node_attributes = (next.y, next.x, next.dir, next.speed)
                if new_node_attributes not in heatlosses or next.heatloss < heatlosses[new_node_attributes]:
                    next_nodes.append(next)
                    heatlosses[new_node_attributes] = next.heatloss

        nodes = next_nodes

    return min([value for (y, x, _, speed), value in heatlosses.items() if y == height - 1 and x == width - 1 and speed >= min_speed])

def part1(lines):
    return compute_heatloss(lines, 1, 3)


def part2(lines):
    return compute_heatloss(lines, 4, 10)


if __name__ == '__main__':

    part = 2
    expectedSampleResult = 94

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
