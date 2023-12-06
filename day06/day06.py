import math
import sys


def parse(filename):
    times, records = open(filename).read().strip().split("\n")
    times = [int(i) for i in times.split()[1:]]
    records = [int(i) for i in records.split()[1:]]
    races = list(zip(times, records))
    return races


def ways_to_beat(races):
    ways_to_beat_record_per_race = []
    for time, record in races:
        ways_to_beat_record = 0
        for hold_time in range(time):
            travel = hold_time * (time - hold_time)
            if travel > record:
                ways_to_beat_record += 1

        ways_to_beat_record_per_race.append(ways_to_beat_record)

    return ways_to_beat_record_per_race


def part1(races):
    return math.prod(ways_to_beat(races))


def part2(races):
    time = int("".join(str(t) for t, _ in races))
    record = int("".join(str(r) for _, r in races))
    return math.prod(ways_to_beat([(time, record)]))


def main():
    filename = "test" if len(sys.argv) == 1 else sys.argv[1]
    races = parse(filename)
    print(part1(races))
    print(part2(races))


main()
