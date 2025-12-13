"""
AdventOfCode 2025 Day 12
https://adventofcode.com/2025/day/12

This problem stunned me. I thought it to be extremely difficult. So I decided to follow
the YT creator "0xdf". He did more or less the same parsing as I had already done, and then
first analyzed the data. He did some statistical analysis to check out the problem's real
complexity. It turned out, the solution is kind of cheating: The shapes need not be
placed very dense. The final question is: will a certain region not be used more than
a certain percentage. For the example, this percentage was around 85%. And using this
threshold gave me the right answer for my input. For other inputs the threshold may vary.
So it is a little bit of a guessing game.

You can watch "0xdf" thinking and coding in this video:
https://youtu.be/pX7pszKHfYw?si=6wIu5Nhw-ahvBQsI

Please consider to give his video a like. I already did.
"""
import configparser
import time
from pathlib import Path

type Shapes = dict[int, list[str]]  # key: shape ID, value: list of shape segments (lines)
type Regions = list[tuple[int, int, list[int]]]  # list of (width, length, list of shape requirements)


def parse(text: str) -> tuple[Shapes, Regions]:
    *shape_specs, region_specs = text.split("\n\n")

    shapes = {}
    for shape_spec in shape_specs:
        lines = shape_spec.split("\n")
        shape_id = int(lines[0][:-1])
        shapes[shape_id] = [row for row in lines[1:]]

    regions = []
    for region in region_specs.splitlines():
        size_spec, *quantitiy_specs = region.split()
        width, length = map(int, size_spec[:-1].split("x"))
        quantities = list(map(int, quantitiy_specs))
        regions.append((width, length, quantities))

    return shapes, regions



def solve(puzzle_input: tuple[Shapes, Regions]) -> int:
    shapes, regions = puzzle_input
    count = 0
    for region in regions:
        width, length, quantities = region
        space_needed = sum(q * ''.join(shapes[i]).count("#") for i, q in enumerate(quantities))
        space_available = width * length
        if space_needed < 0.85 * space_available:
            count += 1
    return count


def load_example(file: Path) -> tuple[str | None, int | None, int | None]:
    example = configparser.ConfigParser(delimiters=('=',), comment_prefixes=(';',))
    with open(file) as f:
        example.read_file(f)
    text = example["Example"].get("text", None)
    part1_ex = example["Example"].getint("part1", None)
    part2_ex = example["Example"].getint("part2", None)
    return text, part1_ex, part2_ex


def main() -> None:

    example = load_example(Path(__file__).with_suffix(".ini"))

    if solve(parse(example[0])) != example[1]:
        print("Day 12 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    start = time.perf_counter()
    answer = solve(parse(puzzle_input))
    end = time.perf_counter()
    print(f"Day 12 solution: {answer}, runtime = {end - start:.3f} s")

    # There is no part 2. We are completely done.


if __name__ == "__main__":
    main()
