"""
AdventOfCode 2025 Day 4
https://adventofcode.com/2025/day/4
"""
import configparser
import time
from pathlib import Path

A_ROLL = "@"

type Pair = tuple[int, int]  # (x, y)


def parse(puzzle_input: str) -> set[Pair]:
    grid = set()
    for y, row in enumerate(puzzle_input.splitlines()):
        for x, tile in enumerate(row):
            if tile == A_ROLL:
                grid.add((x, y))
    return grid


NEIGHBOURSHIP = (  # as (dx, dy) pairs
    (0, -1),  # N
    (1, -1),  # NE
    (1, 0),  # E
    (1, 1),  # SE
    (0, 1),  # S
    (-1, 1),  # SW
    (-1, 0),  # W
    (-1, -1),  # NW
)


def count_neighbors(grid: set[Pair], roll: Pair):
    x, y = roll
    count = 0
    for dx, dy in NEIGHBOURSHIP:
        if (x + dx, y + dy) in grid:
            count += 1
    return count


def solve_part1(puzzle_input: str) -> int:
    grid = parse(puzzle_input)
    answer = 0
    for roll in grid:
        if count_neighbors(grid, roll) < 4:
            answer += 1
    return answer


def find_removable_rolls(grid: set[Pair], neighbour_limit: int = 4) -> set[Pair]:
    candidates = set()
    for roll in grid:
        if count_neighbors(grid, roll) < neighbour_limit:
            candidates.add(roll)
    return candidates


def solve_part2(puzzle_input: str) -> int:
    grid = parse(puzzle_input)
    answer = 0
    while True:
        removable_rolls = find_removable_rolls(grid)
        if not removable_rolls:
            break
        grid -= removable_rolls
        answer += len(removable_rolls)
    return answer


def load_example(file: Path) -> tuple[str | None, int | None, int | None]:
    example = configparser.ConfigParser()
    with open(file) as f:
        example.read_file(f)
    text = example["Example"].get("text", None)
    part1_ex = example["Example"].getint("part1", None)
    part2_ex = example["Example"].getint("part2", None)
    return text, part1_ex, part2_ex


def main() -> None:

    example = load_example(Path(__file__).with_suffix(".ini"))

    assert solve_part1(example[0]) == example[1]

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    start = time.perf_counter()
    answer = solve_part1(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    assert solve_part2(example[0]) == example[2]

    start = time.perf_counter()
    answer = solve_part2(puzzle_input)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
