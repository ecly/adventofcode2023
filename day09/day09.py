import sys


def parse(filename):
    histories = []
    for line in open(filename):
        histories.append([int(i) for i in line.split()])

    return histories


def next_value(history: list[int]) -> int:
    histories = [history]
    while True:
        h = histories[-1]
        deltas = [h - l for l, h in zip(h, h[1:])]
        histories.append(deltas)
        if all(d == 0 for d in deltas):
            break

    histories[-1].append(0)
    for i in range(1, len(histories)):
        current = histories[-i]
        previous = histories[-i - 1]
        previous.append(previous[-1] + current[-1])

    return histories[0][-1]


def part1(histories):
    return sum(next_value(h) for h in histories)


def part2(histories):
    return sum(next_value(h[::-1]) for h in histories)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    histories = parse(filename)
    print(part1(histories))
    print(part2(histories))


if __name__ == "__main__":
    main()
