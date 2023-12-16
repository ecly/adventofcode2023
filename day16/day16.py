import sys
from collections import deque

# x, y, dx, dy
Beam = tuple[int, int, int, int]
Grid = list[str]


def parse(filename) -> Grid:
    with open(filename) as f:
        lines = f.read().strip().split("\n")

    return lines


def turn_right(dx, dy):
    return -dy, dx


def turn_left(dx, dy):
    return dy, -dx


def part1(grid, start: Beam = (-1, 0, 1, 0)):
    beams = deque([start])
    seen = set()
    while beams:
        x, y, dx, dy = beams.popleft()
        if (x, y, dx, dy) in seen:
            continue

        seen.add((x, y, dx, dy))
        nx, ny = x + dx, y + dy
        if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
            continue

        c = grid[ny][nx]
        if c == ".":
            beams.append((nx, ny, dx, dy))
        elif c == "-":
            if dx:
                beams.append((nx, ny, dx, dy))
            else:
                beams.append((nx, ny, -1, 0))
                beams.append((nx, ny, 1, 0))
        elif c == "|":
            if dy:
                beams.append((nx, ny, dx, dy))
            else:
                beams.append((nx, ny, 0, -1))
                beams.append((nx, ny, 0, 1))
        elif c == "|":
            if dy:
                beams.append((nx, ny, dx, dy))
            else:
                beams.append((nx, ny, 0, -1))
                beams.append((nx, ny, 0, 1))
        elif c == "/":
            if dy:
                dx, dy = turn_right(dx, dy)
            else:
                dx, dy = turn_left(dx, dy)
            beams.append((nx, ny, dx, dy))
        elif c == "\\":
            if dy:
                dx, dy = turn_left(dx, dy)
            else:
                dx, dy = turn_right(dx, dy)
            beams.append((nx, ny, dx, dy))

    # subtract one because we start with a node outside the grid
    return len({(x, y) for x, y, _, _ in seen}) - 1


def part2(grid: Grid):
    best = 0
    for y, row in enumerate(grid):
        best = max(best, part1(grid, (-1, y, 1, 0)))
        best = max(best, part1(grid, (len(row), y, -1, 0)))

    for x in range(len(grid[0])):
        best = max(best, part1(grid, (x, -1, 0, 1)))
        best = max(best, part1(grid, (x, len(grid), 0, -1)))

    return best


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    grid = parse(filename)
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
