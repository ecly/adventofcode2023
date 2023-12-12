import heapq
import sys

from tqdm import tqdm


def parse(filename, expansion):
    universe = {}
    for y, line in enumerate(open(filename)):
        line = list(line.strip())
        dist = expansion if all(c == "." for c in line) else 1
        for x, c in enumerate(line):
            universe[x, y] = dist if c == "." else c

    max_x = max(x for x, _ in universe)
    max_y = max(y for _, y in universe)
    for x in range(max_x + 1):
        col = []
        for y in range(max_y + 1):
            col.append(universe[x, y])

        if all(isinstance(c, int) for c in col):
            for y in range(max_y + 1):
                v = expansion * 2 if universe[x, y] == expansion else expansion
                universe[x, y] = v

    return universe


def bfs(universe, a, goals):
    goals = set(goals)
    queue = [(0, a)]
    seen = {a}
    while queue:
        dist, (x, y) = heapq.heappop(queue)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen:
                continue
            if (nx, ny) not in universe:
                continue

            seen.add((nx, ny))
            if (nx, ny) in goals:
                yield dist + 1

            nd = universe[nx, ny]
            if nd == "#":
                nd = 1
            heapq.heappush(queue, (dist + nd, (nx, ny)))


def solve(filename, expansion):
    universe = parse(filename, expansion)
    galaxies = [k for k, v in universe.items() if v == "#"]
    dists = []
    for i, a in tqdm(enumerate(galaxies[:-1]), total=len(galaxies)):
        dists.extend(bfs(universe, a, galaxies[i + 1 :]))

    return sum(dists)


def part1(filename):
    return solve(filename, 2)


def part2(filename):
    return solve(filename, 1000000)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    # each part takes <10s on macbook m2
    print(part1(filename))
    print(part2(filename))


if __name__ == "__main__":
    main()
