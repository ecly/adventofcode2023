import re
import sys
from collections import defaultdict


def parse(filename):
    return open(filename).read().strip().split(",")


def holiday_ascii_string_helper(string: str) -> str:
    v = 0
    for c in string:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def parse_step(step: str) -> tuple[str, str, int | None]:
    m = re.match(r"([a-z]+)([\-=])(\d*)", step)
    return m.group(1), m.group(2), int(m.group(3)) if m.group(3) else None


def part1(steps):
    return sum(holiday_ascii_string_helper(s) for s in steps)


def part2(steps):
    boxes = defaultdict(list)
    for step in steps:
        label, operation, focal_length = parse_step(step)
        box = holiday_ascii_string_helper(label)

        label_in_box = any(b[0] == label for b in boxes[box])

        if operation == "-":
            if label_in_box:
                boxes[box] = [l for l in boxes[box] if l[0] != label]
        else:
            lens = label, focal_length
            if not label_in_box:
                boxes[box].append(lens)
            else:
                boxes[box] = [lens if l[0] == label else l for l in boxes[box]]

    focusing_power = 0
    for box, lenses in boxes.items():
        for i, (label, focal_length) in enumerate(lenses, 1):
            focusing_power += (box + 1) * i * focal_length

    return focusing_power


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    steps = parse(filename)
    print(part1(steps))
    print(part2(steps))


if __name__ == "__main__":
    main()
