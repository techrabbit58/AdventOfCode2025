"""
AdventOfCode 2025 Day 7
https://adventofcode.com/2025/day/7
"""
import copy
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, LiteralString

example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""", 21, 40

SPACE: Final[LiteralString] = "."
SOURCEBEAM: Final[LiteralString] = "S"
BEAM: Final[LiteralString] = "|"
SPLITTER: Final[LiteralString] = "^"

# x: horizontal position of a beam or splitter, 0 ... end of line
# y: vertical position of a beam or splitter, 0 ... (depth - 1)
type Pair = tuple[int, int]  # (x, y)


@dataclass
class Manifold:
    depth: int = field(init=False, default=0)
    beams: dict[int, set[int]] = field(
        init=False, default_factory=lambda: defaultdict(set))
    splitters: dict[int, set[int]] = field(
        init=False, default_factory=lambda: defaultdict(set))
    pathcounts: dict[int, dict[int, int]] = field(
        init=False, default_factory=lambda: defaultdict(lambda: defaultdict(int)))

    def add_beam(self, beam: Pair) -> None:
        self.beams[beam[1]].add(beam[0])
        self.pathcounts[beam[1]][beam[0]] = 1

    def add_splitter(self, splitter: Pair) -> None:
        self.splitters[splitter[1]].add(splitter[0])


def parse(text: str) -> Manifold:
    manifold = Manifold()
    for y, row in enumerate(text.splitlines()):
        manifold.depth = y
        for x, symbol in enumerate(row):
            if symbol == SOURCEBEAM:
                manifold.add_beam((x, y))
            if symbol == SPLITTER:
                manifold.add_splitter((x, y))
    manifold.depth += 1
    return manifold


def solve(manifold: Manifold) -> tuple[int, int]:
    current_beams = manifold.beams[0]
    total_splits = 0

    for level in range(1, manifold.depth):

        splits = manifold.splitters[level] & current_beams
        pathcounts = copy.copy(manifold.pathcounts[level - 1])

        if splits:
            # if we reach this point, tere are one or more splits
            total_splits += len(splits)
            current_beams = current_beams - splits
            for split in splits:
                current_beams.add(split - 1)
                pathcounts[split - 1] += pathcounts[split]
                current_beams.add(split + 1)
                pathcounts[split + 1] += pathcounts[split]
                pathcounts[split] = 0

        manifold.beams[level] = current_beams
        manifold.pathcounts[level] = pathcounts

    total_paths = sum(manifold.pathcounts[manifold.depth - 1].values())

    return total_splits, total_paths


def main() -> None:

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
