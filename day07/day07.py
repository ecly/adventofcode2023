import sys
from collections import Counter
from dataclasses import dataclass
from functools import cached_property

_CARD_MAP = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


@dataclass
class Hand:
    cards: list[int]
    bid: int

    @classmethod
    def from_line(cls, line):
        cards, bid = line.split()
        cards = [int(_CARD_MAP.get(c, c)) for c in cards]
        return cls(cards, int(bid))

    @cached_property
    def strength(self):
        counter = Counter(self.cards)
        c = counter.most_common()
        count1 = c[0][1]
        count2 = None if len(c) == 1 else c[1][1]

        match count1, count2:
            case 5, _:
                return 6
            case 4, _:
                return 5
            case 3, 2:
                return 4
            case 3, _:
                return 3
            case 2, 2:
                return 2
            case 2, _:
                return 1
            case _other:
                return 0

    def __lt__(self, other):
        if self.strength == other.strength:
            return self.cards < other.cards

        return self.strength < other.strength

class JokerHand(Hand):
    @classmethod
    def from_hand(cls, hand: Hand):
        cards = [1 if c == 11 else c for c in hand.cards]
        return cls(cards, hand.bid)

    @cached_property
    def strength(self):
        cards = [c for c in self.cards if c != 1]
        jokers = len(self.cards) - len(cards)
        if not jokers:
            return super().strength

        counter = Counter(cards)
        c = counter.most_common()
        count1 = 0 if len(c) == 0 else c[0][1]
        count2 = 0 if len(c) < 2 else c[1][1]

        match jokers, count1, count2:
            case 1, 4, _:
                return 6
            case 2, 3, _:
                return 6
            case 3, 2, _:
                return 6
            case 4, _, _:
                return 6
            case 5, _, _:
                return 6

            case 1, 3, _:
                return 5
            case 2, 2, _:
                return 5
            case 3, _, _:
                return 5

            case 1, 2, 2:
                return 4
            case 2, 2, _:
                return 4

            case 1, 2, _:
                return 3
            case 2, _, _:
                return 3

            case 1, 2, _:
                return 2

            case _other:
                return 1


def parse(filename) -> list[Hand]:
    return [Hand.from_line(line) for line in open(filename)]


def part1(hands):
    return sum(i * h.bid for i, h in enumerate(sorted(hands), 1))


def part2(hands):
    hands = [JokerHand.from_hand(h) for h in hands]
    return part1(hands)


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    hands = parse(filename)
    print(part1(hands))
    print(part2(hands))


if __name__ == "__main__":
    main()
