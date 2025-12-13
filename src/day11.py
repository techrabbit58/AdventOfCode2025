"""
AdventOfCode 2025 Day 11
https://adventofcode.com/2025/day/11
"""
import configparser
import time
from collections.abc import Callable
from functools import cache
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
    As it looks, all symbols except "out" are exactly once
    a key, and are one or more times on a fanout list.
    """
    lines = [line.split() for line in text.splitlines()]
    return {head[:-1]: tail for head, *tail in lines}


def path_counter(fanouts: dict[str, list[str]]) -> Callable[[str, str], int]:
    """
    The path counter function needs a cache to avoid redundant calculations.
    Unfortunately, "fanout" is not hashable, but I don't like to make it global.
    This closure helps. Have al look at the decorated inner function!
    Now the inner function has an LRU cache, but can work with a local
    extra parameter that cannot be hashed by (and is not relevant for) the cache function.
    """

    @cache
    def count_paths(current: str, terminal: str) -> int:
        if current == terminal:
            return 1

        return sum(count_paths(next_node, terminal) for next_node in fanouts.get(current, []))

    return count_paths


def solve_part1(fanouts: dict[str, list[str]]) -> int:
    count_paths = path_counter(fanouts)
    return count_paths("you", "out")


def solve_part2(fanouts: dict[str, list[str]]) -> int:
    """
    Part 2 suffered from endless runtime and some problem to reach one of both first,
    "dac" or "fft". It was necessary to apply an LRU cache. I also streamlined my path
    counter function (the inner function) after having watched the video of YT creator
    "0xdf" (https://youtu.be/QYdO0pXACOI?si=lSduNlXkKFxzO8Zg). It turned out that it is
    not really necessary to inspect all paths in detail: we do not care for loops.
    """
    count_paths = path_counter(fanouts)

    if count_paths("dac", "fft") == 0:  # there cannot be a bidirectional path (because we are loop-free)
        first, second = "fft", "dac"  # that means: to be loop-free, "fft" must come first
    else:
        first, second = "dac", "fft"  # else, "dac" must come first for the same reason

    return count_paths("svr", first) * count_paths(first, second) * count_paths(second, "out")


def load_example(file: Path) -> tuple[str | None, str | None, int | None, int | None]:
    example = configparser.ConfigParser()
    with open(file) as f:
        example.read_file(f)
    text1_ex = example["Example"].get("text1", None)
    text2_ex = example["Example"].get("text2", None)
    part1_ex = example["Example"].getint("part1", None)
    part2_ex = example["Example"].getint("part2", None)
    return text1_ex, text2_ex, part1_ex, part2_ex


def main() -> None:

    example = load_example(Path(__file__).with_suffix(".ini"))

    if solve_part1(parse(example[0])) != example[2]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    fanouts = parse(puzzle_input)

    start = time.perf_counter()
    answer = solve_part1(fanouts)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(parse(example[1])) != example[3]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(fanouts)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
