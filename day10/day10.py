import sys
from collections import deque

SOUTH = (0, 1)
NORTH = (0, -1)
WEST = (-1, 0)
EAST = (1, 0)
PIPES = {
    "|": [NORTH, SOUTH],
    "-": [EAST, WEST],
    "L": [NORTH, EAST],
    "J": [NORTH, WEST],
    "7": [SOUTH, WEST],
    "F": [SOUTH, EAST],
    ".": [],
    "S": [NORTH, SOUTH, EAST, WEST],
}


def add_connection(grid, c, x, y):
    for dx in range(2):
        for dy in range(2):
            grid[x + dx, y + dy] = set()

    for dx, dy in PIPES[c]:
        grid[x, y].add((x + dx, y + dy))
        # grid[x + dx, y + dy] = set()
        if x + dx >= 0 and y + dy >= 0:
            grid[x + dx, y + dy].add((x + dx * 2, y + dy * 2))


def parse(filename):
    grid = {}
    start = None
    with open(filename) as file_:
        for y, line in enumerate(file_):
            for x, c in enumerate(line.strip()):
                yy = y * 2
                xx = x * 2

                add_connection(grid, c, xx, yy)
                if c == "S":
                    start = xx, yy

    return start, grid


def print_grid(grid, loop=None, enclosed=None):
    max_x = max(x for (x, _), v in grid.items() if v)
    max_y = max(y for (_, y), v in grid.items() if v)
    loop = loop or set()
    enclosed = enclosed or set()
    print("_" * 10)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in loop:
                c = "▒"
            elif (x, y) in enclosed:
                c = "1"
            elif grid[x, y] and x % 2 == 0 and y % 2 == 0:
                c = "█"
            else:
                c = "."
            print(c, end="")
        print()

    print("-" * 10)


def dfs_longest_loop(grid, start):
    queue = deque([(0, start, [start])])
    longest_path = []
    while queue:
        dist, node, seen = queue.popleft()
        for nb in grid[node]:
            if len(seen) > 2 and nb == start:
                if len(seen) + 1 > len(longest_path):
                    seen.append(nb)
                    # print_path(grid, seen)
                    longest_path = seen
                    continue

            if nb in seen or nb not in grid:
                continue

            queue.append((dist + 1, nb, seen + [nb]))

    return longest_path


def part1(start, grid):
    longest_loop = dfs_longest_loop(grid, start)
    return len(longest_loop) // 4, longest_loop


def get_neighbors(x, y):
    return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]


def part2(grid, loop):
    loop = set(loop)
    enclosed = set()
    seen = set()
    starts = [k for k, v in grid.items() if not v]
    for x, y in starts:
        if x % 2 != 0 and y % 2 != 0:
            continue
        if (x, y) in seen:
            continue

        seen.add((x, y))
        queue = deque([(x, y)])
        new_enclosed = {(x, y)}
        is_enclosed = True

        while queue:
            x, y = queue.popleft()
            for nx, ny in get_neighbors(x, y):
                # this area is in our local area
                if (nx, ny) in new_enclosed:
                    continue

                # already checked this area
                if (nx, ny) in enclosed:
                    is_enclosed = False

                # we hit the edge and am thus not in loop
                if (nx, ny) not in grid:
                    is_enclosed = False
                    continue

                # we hit the loop then this is fine
                if (nx, ny) in loop:
                    continue

                new_enclosed.add((nx, ny))
                queue.append((nx, ny))

        seen = seen.union(new_enclosed)
        if is_enclosed:
            enclosed = enclosed.union(new_enclosed)

    print_grid(grid, loop, enclosed)
    return sum(1 for x, y in enclosed if x % 2 == 0 and y % 2 == 0)


def solve(filename):
    start, grid = parse(filename)
    p1_answer, loop = part1(start, grid)
    p2_answer = part2(grid, loop)
    # print(p1_answer, p2_answer)
    return p1_answer, p2_answer


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    p1, p2 = solve(filename)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
