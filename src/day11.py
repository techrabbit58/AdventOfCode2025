"""
AdventOfCode 2025 Day 11
https://adventofcode.com/2025/day/11
"""
import configparser
import time
from pathlib import Path


def parse(text: str) -> dict[str, list[str]]:
    """
    Parse the given list of fanout specifications to a
    dictionary fanouts[current_device]: [next_device, ...].
    There is one single entry with the key "you". This is the
    start of any path to the final output.
    "you" may also be part of multiple fanout specifications.
    There is a fanout "out" that can be part of multiple
    fanout specifications as well, but is giuaranteed never
    being a key to a fanout. So out is a terminal symbol.
    In fact, "out" is the single final output, where every
    valid path terminates.
    There may be paths that never reach "out". These paths
    are invalid (at least for part 1).
    """
    lines = [line.split() for line in text.splitlines()]
    return {head[:-1]: tail for head, *tail in lines}


def count_paths(fanouts: dict[str, list[str]], current: str, path: set[str]) -> int:
    if current == "out":
        return 1

    answer = 0
    for next_device in fanouts[current]:
        if next_device not in path:
            answer += count_paths(fanouts, next_device, path | {current})

    return answer



def solve_part1(fanouts: dict[str, list[str]]) -> int:
    return count_paths(fanouts, "you", set())


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

    ex_fanouts = parse(example[0])

    if solve_part1(ex_fanouts) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    fanouts = parse(puzzle_input)

    start = time.perf_counter()
    answer = solve_part1(fanouts)
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
