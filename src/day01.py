"""
AdventOfCode 2025 Day 1
https://adventofcode.com/2025/day/1
"""
import configparser
import time
from pathlib import Path

FULL_CIRCLE = 100  # 0 to 99


def parse(puzzle_input: str) -> list[int]:
    return [
        (int(rot[1:]) if rot[0] == "R" else (-int(rot[1:])))
        for rot in puzzle_input.split()
    ]


def solve(rotations: list[int]) -> tuple[int, int]:
    dial = 50
    zero_count = zero_transits = 0
    for rotation in rotations:
        # prepare for this step, both parts
        magnitude = abs(rotation)
        sign = rotation // magnitude
        new_dial = dial + sign * magnitude % FULL_CIRCLE  # skip extra circles

        # part 2 - count all zero transits
        zero_transits += magnitude // FULL_CIRCLE  # count extra circles
        # ... and now check if there is one final zero transit
        if dial != 0 and rotation > 0 and new_dial > FULL_CIRCLE:  # count zero visits for R
            zero_transits += 1  # case: add to non-null with carry
        elif dial != 0 and rotation < 0 and new_dial < FULL_CIRCLE:  # count zero visits for L
            zero_transits += 1  # case: subtract from non-null without carry
        elif new_dial == FULL_CIRCLE:  # count direct zero hits by L or R
            zero_transits += 1  # case: add or subtract with result being exactly null

        # part 1
        dial = new_dial % FULL_CIRCLE
        if dial == 0:
            zero_count += 1
    return zero_count, zero_transits


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

    rotations = parse(example[0])
    part1test, part2test = solve(rotations)

    rotations = parse(Path(__file__).with_suffix(".txt").read_text())
    start = time.perf_counter()
    part1solution, part2solution = solve(rotations)
    end = time.perf_counter()

    if part1test == example[1]:
        print("Part 1 solution:", part1solution)
    if part2test == example[2]:
        print("Part 2 solution:", part2solution)

    print(f"runtime <= {(end - start) * 1000:.0f} ms")


if __name__ == "__main__":
    main()
