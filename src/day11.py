"""
AdventOfCode 2025 Day 11
https://adventofcode.com/2025/day/11
"""
import configparser
import time
from pathlib import Path

def parse(text: str):
    ...


def solve_part1(puzzle_input) -> int:
    ...


def solve_part2(puzzle_input) -> int:
    ...


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

    if solve_part1(example[0]) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    start = time.perf_counter()
    answer = solve_part1(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(example[0]) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(puzzle_input)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
