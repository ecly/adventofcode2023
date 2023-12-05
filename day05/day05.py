import sys
from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import Optional


@dataclass
class Destination:
    src_start: int
    dst_start: int
    len: int

    @property
    def offset(self):
        return self.dst_start - self.src_start

    @property
    def src_end(self):
        return self.src_start + self.len

    @property
    def dst_end(self):
        return self.dst_start + self.len

    def merge(self, other: "Destination") -> Optional["Destination"]:
        if self.dst_start >= other.src_end or self.dst_end <= other.src_start:
            return None

        start = max(self.dst_start, other.src_start)
        end = min(self.dst_end, other.src_end)
        src_offset = start - self.dst_start
        dst_offset = start - other.src_start
        return Destination(
            self.src_start + src_offset, other.dst_start + dst_offset, end - start
        )


Maps = list[list[Destination]]


def parse(filename) -> tuple[list[int], Maps]:
    with open(filename) as f:
        sections = f.read().split("\n\n")

    seeds = list(map(int, sections[0].split(": ")[1].split()))
    maps = []
    for sec in sections[1:]:
        destinations = []
        for d in sec.strip().split("\n")[1:]:
            dst_start, src_start, length = map(int, d.split())
            destinations.append(Destination(src_start, dst_start, length))

        maps.append(destinations)

    return seeds, maps


def _merge_destinations(
    fst: list[Destination], snd: list[Destination]
) -> list[Destination]:
    return [m for f, s in product(fst, snd) if (m := f.merge(s))]


def merge_maps(maps: Maps):
    return reduce(_merge_destinations, maps)


def get_lowest_location(seed_ranges: list[tuple[int, int]], maps: Maps):
    merged_map = merge_maps(maps)
    lowest = float("inf")
    for start, length in seed_ranges:
        end = start + length
        for m in merged_map:
            if start >= m.src_end or end <= m.src_start:
                continue

            first_intersect = max(start, m.src_start)
            offset = first_intersect - m.src_start
            location = m.dst_start + offset
            lowest = min(location, lowest)

    return lowest


def part1(seeds: list[int], maps: Maps):
    seed_ranges = [(s, 1) for s in seeds]
    return get_lowest_location(seed_ranges, maps)


def part2(seeds: list[int], maps: Maps):
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    return get_lowest_location(seed_ranges, maps)


def main():
    seeds, maps = parse(sys.argv[1] if len(sys.argv) > 1 else "input")
    print(part1(seeds, maps))
    print(part2(seeds, maps))


if __name__ == "__main__":
    main()
