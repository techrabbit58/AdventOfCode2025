"""
AdventOfCode 2025 Day 5
https://adventofcode.com/2025/day/5
"""
import re
import time
from collections import deque
from operator import itemgetter
from pathlib import Path

example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32""", 3, 14

type Bounds = tuple[int, int]  # (lower, upper)
type IngredientRanges = list[Bounds]  # all ingredient ranges, given by their including bounds
type IngredientList = list[int]  # a list of ingredient IDs


def parse(database: str) -> tuple[IngredientRanges, IngredientList]:
    ingredient_ranges = []
    ingredients = []
    pattern = re.compile(r"(?P<irlow>\d+)-(?P<irhigh>\d+)|(?P<ingred>\d+)")
    for m in pattern.finditer(database):
        match m.groupdict():
            case {"irlow": irlow, "irhigh": irhigh, "ingred": ingred}:
                if ingred is not None:
                    ingredients.append(int(ingred))
                else:
                    ingredient_ranges.append((int(irlow), int(irhigh)))
    return ingredient_ranges, ingredients


def solve_part1(ingredient_ranges: IngredientRanges, ingredients: IngredientList) -> int:
    count = 0
    for ingred in ingredients:
        for irlow, irhigh in ingredient_ranges:
            if irlow <= ingred <= irhigh:
                count += 1
                break
    return count


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    ranges.sort(key=lambda x: x[0])

    merged = []
    current_start, current_end = ranges[0]

    for next_start, next_end in ranges[1:]:
        if next_start <= current_end:
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    merged.append((current_start, current_end))

    return merged


def solve_part2(ingredient_ranges: IngredientRanges) -> int:
    merged = merge_ranges(ingredient_ranges)
    answer = sum(b - a + 1 for a, b in merged)
    return answer


def solve_part2_ugly_version(ingredient_ranges: IngredientRanges) -> int:
    right = deque()
    right.extend(sorted(ingredient_ranges, key=itemgetter(0)))
    left = deque()
    while True:
        if len(right) == 0:  # all work done
            break
        if len(left) == 0:
            left.append(right.popleft())
            continue
        a, b = left[-1], right[0]
        if a[1] < b[0]:
            left.append(right.popleft())
        elif a == b:
            right.popleft()
        elif b[0] <= a[1] <= b[1]:
            left[-1] = a[0], b[1]
            right.popleft()
        else:
            right.popleft()
    answer = sum(b - a + 1 for a, b in left)
    return answer


def main() -> None:
    ex_ranges, ex_ingredients = parse(example[0])

    if solve_part1(ex_ranges, ex_ingredients) != example[1]:
        print("Part 1 failed")

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()
    ingredient_ranges, ingredients = parse(puzzle_input)

    start = time.perf_counter()
    answer = solve_part1(ingredient_ranges, ingredients)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(ex_ranges) != example[2]:
        print("Part 2 failed")

    start = time.perf_counter()
    answer = solve_part2_ugly_version(ingredient_ranges)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
