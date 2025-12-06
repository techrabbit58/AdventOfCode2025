"""
AdventOfCode 2025 Day 6
https://adventofcode.com/2025/day/6
"""
import operator
import time
from functools import reduce
from pathlib import Path

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """, 4277556, None

type Problem = list[str]
type ProblemList = list[Problem]


def parse(text: str) -> ProblemList:
    lines = text.splitlines()
    rows = [row.split() for row in lines]
    num_problems = len(rows[0])

    problems = [[] for _ in range(num_problems)]

    for i, problem in enumerate(problems):
        for row in rows:
            problem.append(row[i])

    return problems


def solve_part1_a(puzzle: ProblemList) -> int:
    """
    WARNING! This is slower, and using eval() on untrustful input
    is dangerous. The eval() function takes its input as python
    source code and then executes it. This can do anything that _you_
    can do on your computer!
    """
    return sum(eval(problem[-1].join(problem[:-1])) for problem in puzzle)


def solve_part1(puzzle: ProblemList) -> int:
    """
    This is a safer solution than slove_part1_a(), and pretty way faster.
    It first translates the
    """
    answer = 0
    for problem in puzzle:
        func, init = {"+": (operator.add, 0), "*": (operator.mul, 1)}[problem[-1]]
        result = reduce(func, map(int, problem[:-1]), init)
        answer += result
    return answer


def solve_part2(puzzle: ProblemList) -> int:
    ...


def main() -> None:

    ex_puzzle = parse(example[0])

    if solve_part1(ex_puzzle) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    puzzle = parse(puzzle_input)

    start = time.perf_counter()
    answer = solve_part1(puzzle)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part1(ex_puzzle) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(puzzle)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
