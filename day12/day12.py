import re
import sys
from functools import lru_cache


def parse(filename):
    rows = []
    for line in open(filename):
        springs, groups = line.strip().split()
        groups = tuple(int(i) for i in groups.split(","))
        rows.append((springs, groups))

    return rows


def is_valid(springs, groups):
    matches = re.findall("#+", springs)
    if len(matches) != len(groups):
        return False

    return all(len(m) == g for m, g in zip(matches, groups))


@lru_cache(1 << 16)
def count_arrangements(springs, groups):
    if not groups:
        return 0 if "#" in springs else 1

    g = groups[0]
    # check if there is any way to match the following group
    m = re.match(rf"^([\.\?]*?)([#\?]{{{g}}})($|\.|\?)(.*)", springs)
    if not m:
        return 0

    prefix, dmg, suffix, rem = m.group(1), m.group(2), m.group(3), m.group(4)
    if "?" in prefix or "?" in dmg or "?" in suffix:
        option1 = count_arrangements(springs.replace("?", ".", 1), groups)
        option2 = count_arrangements(springs.replace("?", "#", 1), groups)
        return option1 + option2

    if "?" in rem:
        return count_arrangements(rem, groups[1:])

    return 1 if is_valid(springs, groups) else 0


def part1(rows):
    return sum(count_arrangements(springs, groups) for springs, groups in rows)


def part2(rows):
    count = 0
    for springs, groups in rows:
        springs_ = "?".join(springs for _ in range(5))
        groups_ = groups * 5
        a = count_arrangements(springs_, groups_)
        count += a

    return count


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    rows = parse(filename)
    print(part1(rows))
    # about 5-10s with python3.11
    print(part2(rows))


if __name__ == "__main__":
    main()
