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
7,3""", 50, 24

type Pixel = tuple[int, int]  # (x, y) as pixel index
type PixelList = list[Pixel]


def parse(text: str) -> PixelList:
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


def solve_part1(pixels: PixelList) -> int:
    max_area = 0

    if len(pixels) < 2:
        return max_area

    for a, b in combinations(pixels, 2):
        max_area = max(max_area, get_square_size(a, b))

    return max_area


def is_point_in_polygon(pixels: PixelList, x, y) -> bool:
    is_inside = False

    for (ax, ay), (bx, by) in zip(pixels, pixels[1:] + pixels[:1]):

        if ((x == ax == bx and min(ay, by) <= y <= max(ay, by)) or
                (y == ay == by and min(ax, bx) <= x <= max(ax, bx))):
            return True

        if ((ay > y) != (by > y)) and (x < (bx - ax) * (y - ay) / (by - ay) + ax):
            is_inside = not is_inside

    return is_inside


def edge_intersects_rect(x1, y1, x2, y2, rx1, ry1, rx2, ry2) -> bool:

    if y1 == y2:
        if ry1 < y1 < ry2:
            if max(x1, x2) > rx1 and min(x1, x2) < rx2:
                return True
    else:
        if rx1 < x1 < rx2:
            if max(y1, y2) > ry1 and min(y1, y2) < ry2:
                return True

    return False


def is_square_valid(pixels: PixelList, a: Pixel, b: Pixel) -> bool:
    x1, x2 = sorted((a[0], b[0]))
    y1, y2 = sorted((a[1], b[1]))

    for x, y in ((x1, y1), (x1, y2), (x2, y1), (x2, y2)):
        if not is_point_in_polygon(pixels, x, y):
            return False

    for (ex1, ey1), (ex2, ey2) in zip(pixels, pixels[1:] + pixels[:1]):
        if edge_intersects_rect(ex1, ey1, ex2, ey2, x1, y1, x2, y2):
            return False

    return True


def solve_part2(pixels: PixelList) -> int:
    """
    Part 1 has been mine, but part 1 is trivial.
    But part 2 was way too hard for me. I needed help.
    This genius part 2 solution, I've borrowed it from YT "0xdf".
    Look at his video to see the brilliant solution that is based
    on a method called "ray finding", or read his original
    code on GitLab: https://gitlab.com/0xdf/aoc2025
    I suggest you consider subscribing to his YT channel and
    at least give his day 9 video a like.
    """
    max_area = 0

    if len(pixels) < 2:
        return max_area

    for a, b in combinations(pixels, 2):
        area = get_square_size(a, b)
        if is_square_valid(pixels, a, b) and area > max_area:
            max_area = area

    return max_area


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
