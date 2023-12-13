import math
import sys


def parse(filename):
    with open(filename) as file_:
        sections = file_.read().split("\n\n")

    patterns = []
    for section in sections:
        grid = {}
        for y, line in enumerate(section.split("\n")):
            for x, c in enumerate(line):
                grid[x, y] = c

        patterns.append(grid)

    return patterns


def is_vertical_reflection(grid, mirror_x, max_y):
    for dx in range(mirror_x):
        for y in range(max_y + 1):
            left = mirror_x - 1 - dx, y
            right = mirror_x + dx, y

            if left not in grid or right not in grid:
                return True

            if grid[left] != grid[right]:
                return False

    return True


def is_horizontal_reflection(grid, mirror_y, max_x):
    for dy in range(mirror_y):
        for x in range(max_x + 1):
            top = x, mirror_y - 1 - dy
            bot = x, mirror_y + dy
            if top not in grid or bot not in grid:
                return True

            if grid[top] != grid[bot]:
                return False

    return True


def analyze_reflection(grid, ignore_x=-1, ignore_y=-1):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    best_x, best_y = 0, 0

    for x in range(max_x + 1):
        if x == ignore_x:
            continue
        if is_vertical_reflection(grid, x, max_y):
            best_x = x

    for y in range(max_y + 1):
        if y == ignore_y:
            continue
        if is_horizontal_reflection(grid, y, max_x):
            best_y = y

    return best_x, best_y


def part1(patterns):
    s = []
    for grid in patterns:
        x, y = analyze_reflection(grid)
        s.append(x + y * 100)

    return sum(s)


def get_smudge(grid):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    base_x, base_y = analyze_reflection(grid)

    for x in range(max_x + 1):
        for y in range(max_y + 1):
            c = grid[x, y]
            grid[x, y] = "." if c == "#" else "."
            rx, ry = analyze_reflection(grid, ignore_x=base_x, ignore_y=base_y)
            grid[x, y] = c
            if rx or ry:
                return rx, ry, x, y


def part2(patterns):
    results = []
    for grid in patterns:
        rx, ry, smudge_x, smudge_y = get_smudge(grid)
        results.append(rx + ry * 100)

    return sum(results)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    patterns = parse(filename)
    print(part1(patterns))
    print(part2(patterns))


if __name__ == "__main__":
    main()
