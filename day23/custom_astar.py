import unittest
from astar import AStar
from day23.basic_astar import BasicAStar


class CustomAStar(AStar):
    def __init__(self, nodes, use_adminissible_heuristic=False, part=1):
        self.nodes = nodes
        self.use_adminissible_heuristic = use_adminissible_heuristic
        self.part = part

    def neighbors(self, n):
        for n1, d in self.nodes[n]:
            yield n1

    def distance_between(self, n1, n2):
        for n, d in self.nodes[n1]:
            if n == n2:
                return d

    def heuristic_cost_estimate(self, current, goal):

        # https://cs.stackexchange.com/questions/28336/longest-path-a-admissible-heuristics-and-optimalness
        # day 23 : adminissible heuristic
        if self.use_adminissible_heuristic:
            if current == goal:
                return 0
            if goal in self.nodes[current]:
                return 1

            if self.part == 1:
              # use a sub A* to find the shortest path between current and goal
              sub_astar = BasicAStar(self.nodes)
              return len(list(sub_astar.astar(current, goal))) * 2
            else:
                # part 2 => use manhattan
                x1, y1 = map(int, current.split(","))
                x2, y2 = map(int, goal.split(","))
                return (abs(x2 - x1) + abs(y2 - y1))



        return 1

    def is_goal_reached(self, current, goal):
        return current == goal

