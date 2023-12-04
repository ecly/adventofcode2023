def _parse_cards(filename="input"):
    games = []
    for line in open(filename):
        card, numbers = line.strip().split(": ")
        winning, mine = numbers.split(" | ")

        winning = {int(i) for i in winning.split()}
        mine = [int(i) for i in mine.split()]
        games.append((winning, mine))

    return games


def part1(games):
    scores = []
    for winning, mine in games:
        matched = [i for i in mine if i in winning]
        if matched:
            scores.append(1 << len(matched) - 1)

    return sum(scores)


def part2(games):
    copy_count = [1] * len(games)
    for i, (winning, mine) in enumerate(games):
        matched = [i for i in mine if i in winning]
        if not matched:
            continue

        current_copies = copy_count[i]
        for j in range(i + 1, i + len(matched) + 1):
            copy_count[j] += current_copies

    return sum(copy_count)


def main():
    games = _parse_cards("test")
    print(part1(games))
    print(part2(games))


if __name__ == "__main__":
    main()
