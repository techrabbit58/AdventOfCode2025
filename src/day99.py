from pathlib import Path

example = """
"""


class Solution:
    def __init__(self, puzzle_input: str) -> None:
        ...

    def part1(self) -> int:
        ...

    def part2(self) -> int:
        ...


def main(puzzle_input: str) -> None:
    solution = Solution(example)
    print("Part 1 solution:", solution.part1())

    text = Path(puzzle_input).read_text()
    print("Part 2 solution:", solution.part2())


if __name__ == "__main__":
    main("day99.txt")
