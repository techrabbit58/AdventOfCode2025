"""
AdventOfCode 2025 Day 6
https://adventofcode.com/2025/day/6
"""
import operator
import re
import time
from collections.abc import Callable
from functools import reduce
from pathlib import Path

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """, 4277556, 3263827

type Problem = list[str]
type ProblemList = list[Problem]
type ParseFunc = Callable[[str], ProblemList]

PATTERN = re.compile(r"([+*]\s*)")


def parse_for_part1(text: str) -> ProblemList:
    lines = [line + " " for line in text.splitlines()]
    operators = PATTERN.findall(lines[-1])
    sizes = [len(op) - 1 for op in operators]

    rows = []
    for row in lines:
        rows.append([])
        i = 0
        for size in sizes:
            rows[-1].append(row[i: i + size])
            i += size + 1

    num_problems = len(rows[0])

    problems = [[] for _ in range(num_problems)]

    for i, problem in enumerate(problems):
        for row in rows:
            problem.append(row[i])

    return problems


def transpose(raw_numbers: Problem) -> Problem:
    num_positions = len(raw_numbers[0])
    transposed_digits = [[] for _ in range(num_positions)]
    for i, transposed in enumerate(transposed_digits):
        for symbols in raw_numbers:
            transposed.append(symbols[num_positions - i - 1])
    transposed_numbers = ["".join(digits) for digits in transposed_digits]
    return transposed_numbers


def parse_for_part2(text: str) -> ProblemList:
    raw_problems = parse_for_part1(text)
    operands = [problem[-1] for problem in raw_problems]
    transposed_numbers = [transpose(problem[:-1]) for problem in raw_problems]
    problems = [nums + [op] for op, nums in zip(operands, transposed_numbers)]
    return problems


def solve(puzzle_input: str, parse: ParseFunc) -> int:
    """
    (1) Transform the puzzle input to a list of problem records. A problem record
    is a list of strings where all but the last element represent positive integer
    numbers, and the last element represents one of "+" or "*" for addition or
    multiplication. Example: ["123 ", "4   ", "31  ", "3446", "+   "].
    (2) Add or multiply all numbers in a problem. Example: result = 123 + 4 +31 + 3446.
    (3) Add all results up to the answer.
    (4) Return the answer to the caller.
    :param puzzle_input: A text file, organized as equal length lines
        (spaces are significant)
    :param parse: A function that can transform the given puzzle input to
        a list of problem records
    :return: the answer to the puzzle as a single integer number
    """
    problems = parse(puzzle_input)
    answer = 0
    for problem in problems:
        func, init = {"+": (operator.add, 0), "*": (operator.mul, 1)}[problem[-1].strip()]
        result = reduce(func, map(int, problem[:-1]), init)
        answer += result
    return answer


def main() -> None:

    if solve(example[0], parse_for_part1) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    start = time.perf_counter()
    answer = solve(puzzle_input, parse_for_part1)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve(example[0], parse_for_part2) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve(puzzle_input, parse_for_part2)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
