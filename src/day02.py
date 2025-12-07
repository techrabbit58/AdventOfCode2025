"""
AdventOfCode 2025 Day 2
https://adventofcode.com/2025/day/2

Part 1: In an inclusive range of positive decimal integer numbers [i, j], find all
numbers that follow a certain pattern of digits: ([1-9][0-9]~n)~2. That means:
a matching number must have an even number of decimal digits, and its first half
must repeat exactly once as the second half. For instance, 123123 -> 123|123 does
fit the pattern, but 123321 or 123456 do not.

Part 2: This is basically the same as part 1, but the pattern differs slightly so that
111 is now a valid pattern (1|1|1), or 123123123 (123|123|123). There may be repeated
sequences of any length from 1 to length/2. All sequences must be fully repeated.
Minimum repetition is 1 + 1 for length/2, 1 + 2 for langth/3 and so on. All sequences
and repeated sequences together must compose to a full match. For instance,
123|123|123|4 isn't a full match, because there is an extra digit without a match.
12|12|12|2|12 is not a match, because there is one incomplete sequence in the middle.
1234|1234|123 is not a match because the last sequence is not complete.
"""
import re
import time
from pathlib import Path

example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124""", 1227775554, 4174379265


def parse(text: str) -> list[tuple[int, int]]:
    result = []
    for pair in re.split(r",\s*", text):
        a, b = [int(n) for n in pair.split("-")]
        result.append((a, b))
    return result


def solve(id_ranges: list[tuple[int, int]], pattern: re.Pattern) -> int:
    answer = 0
    for first, last in id_ranges:
        for i in range(first, last + 1):
            digits = str(i)
            if pattern.fullmatch(digits):
                answer += i
    return answer


def main() -> None:
    example_ranges = parse(example[0])

    part1pattern = re.compile(r"([1-9][0-9]*)\1")

    assert solve(example_ranges, part1pattern) == example[1]

    text = Path(__file__).with_suffix(".txt").read_text()
    puzzle_ranges = parse(text)

    start = time.perf_counter()
    part1solution = solve(puzzle_ranges, part1pattern)
    end = time.perf_counter()

    print(f"Part 1 solution: {part1solution}, runtime = {end - start:.3f} s")

    part2pattern = re.compile(r"([1-9][0-9]*)\1+")

    assert solve(example_ranges, part2pattern) == example[2]

    start = time.perf_counter()
    part2solution = solve(puzzle_ranges, part2pattern)
    end = time.perf_counter()

    print(f"Part 2 solution: {part2solution}, runtime = {end - start:.3f} s")

if __name__ == "__main__":
    main()
