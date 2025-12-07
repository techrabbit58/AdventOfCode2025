"""
AdventOfCode 2025 Day 5
https://adventofcode.com/2025/day/5
"""
import re
import time
from collections import deque
from collections.abc import Callable
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

type SortableSequence = list | deque
type Bounds = tuple[int, int]  # (lower, upper)
type IngredientRanges = SortableSequence[Bounds]  # ingredient ranges
type IngredientList = list[int]  # a list of ingredient IDs
type RangeMerger = Callable[[IngredientRanges], IngredientRanges]


def parse(database: str) -> tuple[IngredientRanges, IngredientList]:
    ingredient_ranges = []
    ingredients = []
    pattern = re.compile(r"(?P<irlow>\d+)-(?P<irhigh>\d+)|(?P<ingred>\d+)")
    for m in pattern.finditer(database):
        match m.groupdict():
            case {"irlow": None, "irhigh": None, "ingred": ingred}:
                ingredients.append(int(ingred))
            case {"irlow": irlow, "irhigh": irhigh, "ingred": None}:
                ingredient_ranges.append((int(irlow), int(irhigh)))
            case _:
                raise RuntimeError(f"Incompatible token: {m.groupdict()}")
    return ingredient_ranges, ingredients


def solve_part1(ingredient_ranges: IngredientRanges, ingredients: IngredientList) -> int:
    count = 0
    for ingred in ingredients:
        for irlow, irhigh in ingredient_ranges:
            if irlow <= ingred <= irhigh:
                count += 1
                break
    return count


def merge(ranges: IngredientRanges) -> IngredientRanges:
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


def ugly_merge(ranges: IngredientRanges) -> IngredientRanges:
    right = deque()
    right.extend(sorted(ranges, key=itemgetter(0)))
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
        elif b[0] <= a[1] <= b[1]:
            left[-1] = a[0], b[1]
            right.popleft()
        else:
            right.popleft()
    return left


def solve_part2(ingredient_ranges: IngredientRanges, mergefunc: RangeMerger) -> int:
    merged = mergefunc(ingredient_ranges)
    answer = sum(b - a + 1 for a, b in merged)
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

    if solve_part2(ex_ranges, merge) != example[2]:
        print("Part 2 failed")

    start = time.perf_counter()
    answer = solve_part2(ingredient_ranges, merge)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
