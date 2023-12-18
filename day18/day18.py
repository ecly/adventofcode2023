import sys
from collections import deque

directions = {"R": 1, "L": -1, "U": -1j, "D": 1j}


def print_grid(grid):
    max_x = int(max(p.real for p in grid))
    max_y = int(max(p.imag for p in grid))
    print("_" * 10)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if x + y * 1j in grid:
                c = "#"
            else:
                c = "."
            print(c, end="")
        print()

    print("-" * 10)


def parse(filename):
    grid = {}
    pos = 0j
    for line in open(filename):
        direction, amount, color = line.strip().split()
        delta = directions.get(direction)
        for _ in range(int(amount)):
            pos += delta
            grid[pos] = color

    print_grid(grid)
    return grid


def part1(grid):
    start = 1+1j
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

def part2(grid):
    pass


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    grid = parse(filename)
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
