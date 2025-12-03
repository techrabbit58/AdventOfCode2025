"""
AdventOfCode 2025 Day 3
"""
import time
from collections import deque
from pathlib import Path

example = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines(), 357, 3121910778619


def find_max_pair_joltage(segment: str, depth: int = 2) -> list[int]:
    if depth == 0:
        return []

    middle = 0
    index = 0
    for i, digit in enumerate(segment):
        n = int(digit)
        if middle < n:
            middle = n
            index = i
    if middle == 0:
        return []

    right = find_max_pair_joltage(segment[index + 1:], depth - 1)
    left = find_max_pair_joltage(segment[:index], depth - 1)
    digits = left + [middle] + right

    if len(digits) > 2 and digits[0] < digits[1]:
        return digits[1:]
    else:
        return digits[:2]


def solve_part1(banks: list[str], depth: int = 2) -> int:
    answer = 0
    for bank in banks:
        answer += int(''.join(str(n) for n in find_max_pair_joltage(bank, depth)))
    return answer


def find_max_multi_joltage(segment: str, size: int) -> deque[int]:
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

    result.extend(find_max_multi_joltage(right, size - 1))

    if len(result) >= size:
        return result

    left_result = find_max_multi_joltage(left, size - len(result))
    result.extendleft(reversed(left_result))

    return result



def solve_part2(banks: list[str], size: int = 2) -> int:
    answer = 0
    for bank in banks:
        answer += int("".join(map(str, find_max_multi_joltage(bank, size))))
    return answer


def main() -> None:
    assert solve_part2(example[0]) == example[1]

    puzzle_input = Path(__file__).with_suffix(".txt").read_text().splitlines()

    start = time.perf_counter()
    answer = solve_part2(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    size = 12
    assert solve_part2(example[0], size=size) == example[2]

    start = time.perf_counter()
    answer = solve_part2(puzzle_input, size=size)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
