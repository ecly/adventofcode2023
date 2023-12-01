import regex as re


def part1():
    nums = []
    for line in open("input"):
        n = [i for i in re.findall(r"\d", line)]
        nums.append(int(n[0] + n[-1]))

    return sum(nums)


def part2():
    str_to_int = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    nums = []
    for line in open("input"):
        pattern = rf"({'|'.join(str_to_int)}|\d)"
        n = [i for i in re.findall(pattern, line, overlapped=True)]
        nums.append(int(str_to_int.get(n[0], n[0]) + str_to_int.get(n[-1], n[-1])))
        if "eightwo" in line:
            print(nums[-1])

    return sum(nums)


print(part1())
print(part2())
