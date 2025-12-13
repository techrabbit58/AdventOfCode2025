"""
AdventOfCode 2025 Day 3
https://adventofcode.com/2025/day/3
"""
import configparser
import time
from collections import deque
from pathlib import Path


def find_max(segment: str, size: int) -> deque[int]:
    result = deque()
    if size == 0 or not segment:
        return result

    pivot = 0
    for d in segment:
        n = int(d)
        if pivot < n:
            pivot = n

    left, right = segment.split(str(pivot), 1)
    result.append(pivot)

    result.extend(find_max(right, size - 1))

    if len(result) >= size:
        return result

    left_result = find_max(left, size - len(result))
    result.extendleft(reversed(left_result))

    return result


def load_example(file: Path) -> tuple[str | None, int | None, int | None]:
    example = configparser.ConfigParser()
    with open(file) as f:
        example.read_file(f)
    text = example["Example"].get("text", None)
    part1_ex = example["Example"].getint("part1", None)
    part2_ex = example["Example"].getint("part2", None)
    return text, part1_ex, part2_ex


def solve(banks: list[str], size: int = 2) -> int:
    answer = 0
    for bank in banks:
        answer += int("".join(map(str, find_max(bank, size))))
    return answer


def main() -> None:

    example = load_example(Path(__file__).with_suffix(".ini"))

    assert solve(example[0].splitlines()) == example[1]

    puzzle_input = Path(__file__).with_suffix(".txt").read_text().splitlines()

    start = time.perf_counter()
    answer = solve(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    size = 12
    assert solve(example[0].splitlines(), size=size) == example[2]

    start = time.perf_counter()
    answer = solve(puzzle_input, size=size)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
