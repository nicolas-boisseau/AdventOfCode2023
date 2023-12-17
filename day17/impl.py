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
    def __init__(self, y, x, dir, speed, heatloss, lines, history):
        self.y = y
        self.x = x
        self.dir = dir
        self.lines = lines
        self.speed = speed
        self.heatloss = heatloss
        self.history = history + [(y, x, dir)]

    def forward(self):
        if self.speed < 3:
            new_y = self.y + directions[self.dir][0]
            new_x = self.x + directions[self.dir][1]
            if self.is_out_of_bounds(new_y, new_x) or (new_y, new_x, self.dir) in self.history:
                return []
            new_speed = self.speed + 1
            new_heatloss = self.heatloss + int(self.lines[new_y][new_x])
            return [
                Node(new_y, new_x, self.dir, new_speed, new_heatloss, self.lines, self.history),
            ]
        return []


    def left(self):
        new_dir = new_directions[self.dir][0]
        new_y = self.y + directions[new_dir][0]
        new_x = self.x + directions[new_dir][1]
        if self.is_out_of_bounds(new_y, new_x) or (new_y, new_x, new_dir) in self.history:
            return []
        new_speed = 1
        new_heatloss = self.heatloss + int(self.lines[new_y][new_x])
        return [
            Node(new_y, new_x, new_dir, new_speed, new_heatloss, self.lines, self.history),
        ]
    def right(self):
        new_dir = new_directions[self.dir][1]
        new_y = self.y + directions[new_dir][0]
        new_x = self.x + directions[new_dir][1]
        if self.is_out_of_bounds(new_y, new_x) or (new_y, new_x, new_dir) in self.history:
            return []
        new_speed = 1
        new_heatloss = self.heatloss + int(self.lines[new_y][new_x])
        return [
            Node(new_y, new_x, new_dir, new_speed, new_heatloss, self.lines, self.history),
        ]

    def is_out_of_bounds(self, y, x):
        return y < 0 or y >= len(self.lines) or x < 0 or x >= len(self.lines[0])

    def finished(self):
        return self.y == len(self.lines) - 1 and self.x == len(self.lines[0]) - 1

    def __repr__(self):
        return f"Node({self.y}, {self.x}, {self.dir}, {self.speed}, {self.heatloss}, {self.lines}, {self.history})"

    def print(self):
        print(f"Node({self.y}, {self.x}, {self.dir}, {self.speed}, {self.heatloss}, {self.lines}, {self.history})")
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if (y, x, "N") in self.history:
                    print("^", end="")
                elif (y, x, "E") in self.history:
                    print(">", end="")
                elif (y, x, "S") in self.history:
                    print("v", end="")
                elif (y, x, "W") in self.history:
                    print("<", end="")
                else:
                    print(char, end="")
            print()
        print()


def part1(lines):
    rows = len(lines)
    cols = len(lines[0])

    possible_paths = [
        Node(0, 0, "E", 0, 0, lines, []),
        Node(0, 0, "S", 0, 0, lines, [])
    ]
    finished_paths = []
    already_seen = {}
    while len(possible_paths) > 0:
        current_path = possible_paths[0]
        possible_paths = possible_paths[1:]

        next_nodes = current_path.forward()
        next_nodes += current_path.left()
        next_nodes += current_path.right()

        for new_node in next_nodes:
            new_node_attributes = (new_node.y, new_node.x)
            if len(finished_paths) > 0 and new_node.heatloss >= finished_paths[0].heatloss:
                continue
            if new_node_attributes not in already_seen:
                possible_paths.append(new_node)
                already_seen[new_node_attributes] = new_node.heatloss
            elif new_node.heatloss < already_seen[new_node_attributes]:
                possible_paths.append(new_node)
                already_seen[new_node_attributes] = min(already_seen[new_node_attributes], new_node.heatloss)
        #print_possible_paths(possible_paths, lines)
        finished_paths += [p for p in possible_paths if p.finished()]
        finished_paths.sort(key=lambda p: p.heatloss)

        print(f"Finished paths : {len(finished_paths)}")
        if len(finished_paths) > 0:
            print(f"Current best : {finished_paths[0].heatloss}")

    finished_paths[0].print()
    return finished_paths[0].heatloss #already_seen[(rows-1,cols-1)]






def part2(lines):
    return 4


if __name__ == '__main__':

    part = 1
    expectedSampleResult = 102

    part_func = part1 if part == 1 else part2
    if part_func(read_input_lines("sample.txt")) == expectedSampleResult:
        print(f"Sample for part {part} OK")

        result = part_func(read_input_lines("input.txt"))
        print(f"Input result for part {part} is {result}")

        post_answer(2023, part, result)
        print(f"Part {part} result posted !")
