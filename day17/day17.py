import heapq
import sys


def parse(filename):
    with open(filename) as f:
        lines = f.read().strip().split("\n")

    rows = []
    for line in lines:
        rows.append([int(c) for c in line])

    return rows


def tail_directional_length(path):
    dx, dy = None, None
    c = 0
    for (ax, ay), (bx, by) in zip(path[::-1], path[-2::-1]):
        ndx = ax - bx
        ndy = ay - by
        if dx is not None:
            if ndx != dx or ndy != dy:
                break

        c += 1
        dx, dy = ndx, ndy

    return c


def solve(grid, min_straight, max_straight):
    start = 0, 0
    queue = [(0, start, [start])]
    goal = len(grid[-1]) - 1, len(grid) - 1
    seen = set()
    while queue:
        dist, (x, y), path = heapq.heappop(queue)
        if (x, y) == goal:
            return dist

        dirs = []
        if len(path) > 1:
            (t1x, t1y), (t2x, t2y) = path[-2:]
            pdx, pdy = t2x - t1x, t2y - t1y
        else:
            pdx, pdy = 1, 1

        if pdx:  # we previously moved along X
            dirs.extend([(0, -1), (0, 1)])
        if pdy:  # we previously moved along Y
            dirs.extend([(-1, 0), (1, 0)])

        for delta in range(min_straight, max_straight + 1):
            for dx, dy in dirs:
                nd = 0
                nx, ny = x, y
                out_of_grid = False

                stride = []
                for i in range(delta):
                    nx, ny = nx + dx, ny + dy
                    stride.append((nx, ny))
                    if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                        out_of_grid = True
                        break

                    nd += grid[ny][nx]

                if out_of_grid:
                    continue

                new_path = path + stride
                # a better check/signature for whether we've seen
                # a tail here could make it significantly faster
                tail = tuple(new_path[-(max_straight+1):])
                if tail in seen:
                    continue

                seen.add(tail)
                heapq.heappush(queue, (dist + nd, (nx, ny), new_path))


def part1(grid):
    return solve(grid, min_straight=1, max_straight=3)


def part2(grid):
    return solve(grid, min_straight=4, max_straight=10)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    grid = parse(filename)
    # about 60s to run both, due to inefficient checking fo visited states
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
