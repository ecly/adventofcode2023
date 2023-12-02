from collections import defaultdict


def _parse_game_line(line) -> list[dict[str, int]]:
    game, pulls_str = line.split(":")
    pulls = []
    for pull in pulls_str.split(";"):
        cubes = defaultdict(int)
        for cubes_str in pull.split(","):
            count, color = cubes_str.split()
            cubes[color] += int(count)

        pulls.append(cubes)

    _, game_id = game.split()
    return int(game_id), pulls


def part1(games):
    possible_games = []
    for game_id, pulls in games:
        if all(c["red"] <= 12 and c["green"] <= 13 and c["blue"] <= 14 for c in pulls):
            possible_games.append(game_id)

    return sum(possible_games)


def part2(games):
    cube_powers = []
    for game_id, pulls in games:
        min_red = max(c["red"] for c in pulls)
        min_green = max(c["green"] for c in pulls)
        min_blue = max(c["blue"] for c in pulls)
        cube_powers.append(min_red * min_green * min_blue)

    return sum(cube_powers)


games = [_parse_game_line(line) for line in open("input")]
print(part1(games))
print(part2(games))
