"""
AdventOfCode 2025 Day 7
https://adventofcode.com/2025/day/7
"""
import configparser
import copy
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, LiteralString

SPACE: Final[LiteralString] = "."
SOURCEBEAM: Final[LiteralString] = "S"
BEAM: Final[LiteralString] = "|"
SPLITTER: Final[LiteralString] = "^"


@dataclass
class Manifold:
    depth: int = field(init=False, default=0)
    initial_beam: int = field(init=False, default=-1)
    splitters: dict[int, set[int]] = field(
        init=False, default_factory=lambda: defaultdict(set))
    pathcounts: dict[int, dict[int, int]] = field(
        init=False, default_factory=lambda: defaultdict(lambda: defaultdict(int)))

    def set_initial_beam(self, x: int, y: int) -> None:
        self.initial_beam = x
        self.pathcounts[y][x] = 1

    def add_splitter(self, x: int, y: int) -> None:
        self.splitters[y].add(x)


def parse(text: str) -> Manifold:
    manifold = Manifold()
    for y, row in enumerate(text.splitlines()):
        manifold.depth = y
        for x, symbol in enumerate(row):
            if symbol == SOURCEBEAM:
                manifold.set_initial_beam(x, y)
            if symbol == SPLITTER:
                manifold.add_splitter(x, y)
    manifold.depth += 1
    return manifold


def solve(manifold: Manifold) -> tuple[int, int]:
    current_beams = {manifold.initial_beam}
    total_splits = 0

    for level in range(1, manifold.depth):

        splits = manifold.splitters[level] & current_beams
        pathcounts = copy.copy(manifold.pathcounts[level - 1])

        if splits:
            # if we reach this point, there are one or more splits
            # part 1
            total_splits += len(splits)
            current_beams = current_beams - splits

            # part 2
            for split in splits:
                current_beams.add(split - 1)
                pathcounts[split - 1] += pathcounts[split]
                current_beams.add(split + 1)
                pathcounts[split + 1] += pathcounts[split]
                pathcounts[split] = 0

        manifold.pathcounts[level] = pathcounts

    total_paths = sum(manifold.pathcounts[manifold.depth - 1].values())

    return total_splits, total_paths


def load_example(file: Path) -> tuple[str | None, int | None, int | None]:
    example = configparser.ConfigParser()
    with open(file) as f:
        example.read_file(f)
    text = example["Example"].get("text", None)
    part1_ex = example["Example"].getint("part1", None)
    part2_ex = example["Example"].getint("part2", None)
    return text, part1_ex, part2_ex


def main() -> None:

    example = load_example(Path(__file__).with_suffix(".ini"))

    ex_manifold = parse(example[0])

    if solve(ex_manifold)[0] != example[1]:
        print("Part 1 not done")
        exit()

    manifold = parse(Path(__file__).with_suffix(".txt").read_text())

    start = time.perf_counter()
    part1, part2 = solve(manifold)
    end = time.perf_counter()
    print(f"Part 1 solution: {part1}")

    if solve(ex_manifold)[1] != example[2]:
        print("Part 2 not done")
        exit()

    print(f"Part 2 solution: {part2}")

    print(f"total runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
