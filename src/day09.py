"""
AdventOfCode 2025 Day 9
https://adventofcode.com/2025/day/9
"""
import re
import time
from itertools import combinations
from pathlib import Path

example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 50, None

type Pixel = tuple[int, int]  # (x, y) as pixel index


def parse(text: str) -> list[Pixel]:
    lines = text.splitlines()
    pixels = []
    for line in lines:
        xy = re.findall(r"(\d+)", line)
        if len(xy) != 2:
            raise ValueError(f"Too many numbers in line: {line}")
        x, y = map(int, xy)
        pixels.append((x, y))
    return pixels


def get_square_size(a: Pixel, b:Pixel) -> int:
    (ax, ay), (bx, by) = a, b
    return (abs(ax - bx) + 1) * (abs(ay - by) + 1)


def solve_part1(pixels: list[Pixel]) -> int:
    max_area = 0

    if len(pixels) < 2:
        return max_area

    for a, b in combinations(pixels, 2):
        max_area = max(max_area, get_square_size(a, b))

    return max_area


def solve_part2(puzzle_input) -> int:
    ...


def main() -> None:
    ex_pixels = parse(example[0])

    if solve_part1(ex_pixels) != example[1]:
        print("Part 1 not done")
        exit()

    pixels = parse(Path(__file__).with_suffix(".txt").read_text())

    start = time.perf_counter()
    answer = solve_part1(pixels)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(ex_pixels) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(pixels)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
