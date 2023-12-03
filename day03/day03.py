import math
import re


def parse(filename="test"):
    grid = {}
    for y, line in enumerate(open(filename)):
        for x, c in enumerate(line.strip()):
            grid[x, y] = c

        for match in re.finditer(r"\d+", line):
            start, end = match.span()
            n = int(match.group())
            for x in range(start, end):
                grid[x, y] = (start, y, n)

    return grid


def part1(grid):
    parts = set()
    for (x, y), c in grid.items():
        if isinstance(c, tuple) or c == ".":
            continue

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                pos = (x + dx, y + dy)
                value = grid.get(pos)
                if isinstance(value, tuple):
                    parts.add(value)

    return parts, sum(part_number for (_, _, part_number) in parts)


def part2(grid, parts):
    gear_ratios = []
    for (x, y), c in grid.items():
        if c != "*":
            continue

        adjacent_parts = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                pos = (x + dx, y + dy)
                value = grid.get(pos)
                if isinstance(value, tuple) and value in parts:
                    adjacent_parts.add(value)

        if len(adjacent_parts) == 2:
            gear_ratios.append(math.prod(v[-1] for v in adjacent_parts))

    return sum(gear_ratios)


def main():
    grid = parse("input")
    parts, parts_sum = part1(grid)
    print(parts_sum)
    print(part2(grid, parts))


if __name__ == "__main__":
    main()
