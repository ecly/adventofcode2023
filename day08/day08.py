import math
import re
import sys
from itertools import cycle


def parse(filename):
    nodes = {}
    lines = open(filename).read().strip().split("\n")
    instructions = lines[0]
    for line in lines[2:]:
        match = re.match(r"(\w+) = \((\w+), (\w+)\)", line.strip())
        nodes[match.group(1)] = (match.group(2), match.group(3))

    return instructions, nodes


def part1(instructions, nodes):
    position = "AAA"
    for i, move in enumerate(cycle(instructions), 1):
        l, r = nodes[position]
        position = l if move == "L" else r
        if position == "ZZZ":
            return i


def part2(instructions, nodes):
    positions = [n for n in nodes if n.endswith("A")]
    steps_to_z = []
    for p in positions:
        for i, move in enumerate(cycle(instructions), 1):
            l, r = nodes[p]
            p = l if move == "L" else r
            if p.endswith("Z"):
                steps_to_z.append(i)
                break

    return math.lcm(*steps_to_z)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    instructions, nodes = parse(filename)
    print(part1(instructions, nodes))
    print(part2(instructions, nodes))


if __name__ == "__main__":
    main()
