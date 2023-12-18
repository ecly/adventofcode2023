import sys
from collections import deque

directions = {"R": 1, "L": -1, "U": -1j, "D": 1j}


def parse_part1(filename):
    grid = {}
    pos = 0j
    for line in open(filename):
        direction, amount, color = line.strip().split()
        delta = directions.get(direction)
        for _ in range(int(amount)):
            pos += delta
            grid[pos] = color

    return grid


def part1(filename):
    grid = parse_part1(filename)

    start = 1 + 1j
    queue = deque([start])
    seen = set()
    while queue:
        pos = queue.popleft()
        for d in directions.values():
            new_pos = pos + d
            if new_pos in seen or new_pos in grid:
                continue
            seen.add(new_pos)
            queue.append(new_pos)
    return len(grid) + len(seen)

def parse_part2(filename):
    points = []
    pos = 0j

def part2(grid):
    for line in open(filename):
        direction, amount, color = line.strip().split()
        delta = directions.get(direction)
        for _ in range(int(amount)):
            pos += delta
            grid[pos] = color

    return grid

    pass


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    print(part1(filename))
    print(part2(filename))


if __name__ == "__main__":
    main()
