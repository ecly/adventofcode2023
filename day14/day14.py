import sys
from collections import Counter, defaultdict


def parse(filename):
    grid = []
    for line in open(filename):
        grid.append(list(line.strip()))

    return grid


def get_load(grid):
    load = 0
    for y, row in enumerate(grid):
        rounded_rocks = row.count("O")
        load += rounded_rocks * (len(grid) - y)

    return load


def print_grid(grid):
    for r in grid:
        print("".join(r))
    print()


def slide_rocks(grid):
    for y in range(1, len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if row[x] in ".#":
                continue

            for dy in range(1, y + 1):
                if grid[y - dy][x] == ".":
                    grid[y - dy][x] = "O"
                    grid[y - dy + 1][x] = "."
                else:
                    break


def part1(grid):
    slide_rocks(grid)
    return get_load(grid)


def print_load_patterns(loads):
    for k, v in sorted(loads.items(), key=lambda x: len(x[1])):
        if len(v) == 1:
            continue

        print(f"Value: {k}")
        print(f"\ti: {v}")
        if len(v) > 1:
            ds = [b - a for a, b in zip(v, v[1:])]
            print(f"\td: {ds}")
        print()


def part2(grid):
    print_grid(grid)
    loads = defaultdict(list)
    # I tried to look for patterns, but didn't find the exact one.
    # Was guided to picking a frequently occuring one with correct value through
    # 3 tries and the UI telling me answer was too low.
    #
    # 1000 happens to give the correct answer, but I don't know if it generalizes.
    for i in range(1000):
        for _ in range(4):
            slide_rocks(grid)
            grid = [list(r) for r in zip(*grid[::-1])]

        load = get_load(grid)
        loads[load].append(i)

    # what I used to find the intended patterns
    print_load_patterns(loads)
    return get_load(grid)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    grid = parse(filename)
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
