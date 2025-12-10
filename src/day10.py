"""
AdventOfCode 2025 Day 10
https://adventofcode.com/2025/day/10
"""
import time
from pathlib import Path

example = """""", None, None


def parse(text: str):
    ...


def solve_part1(puzzle_input) -> int:
    ...


def solve_part2(puzzle_input) -> int:
    ...


def main() -> None:
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
