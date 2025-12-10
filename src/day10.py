"""
AdventOfCode 2025 Day 10
https://adventofcode.com/2025/day/10
"""
import re
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""", 7, 33


@dataclass
class Machine:
    serial: int = field(kw_only=True)
    target_state: int
    buttons: list[int]
    joltages: list[int]
    lights_width: int = field(repr=False, kw_only=True)


def parse(text: str) -> list[Machine]:
    machines = []
    for serial, line in enumerate(text.splitlines(), 1):
        target_state = 0
        width = 0
        for i, c in enumerate(reversed(re.search(r"\[(?P<ind>[.#]+),?]", line).group("ind"))):
            if c == "#":
                target_state |= 1 << i
            width = i
        width += 1
        buttons = []
        for button in re.findall(r"(\(.+?\))", line):
            wiring = 0
            for n in re.findall(r"(\d+)", button):
                wiring |= 1 << (width - int(n) - 1)
            buttons.append(wiring)
        joltages = [int(n) for n in re.search(r"\{(?P<jol>(\d+,?)+)}", line).group("jol").split(",")]
        machines.append(Machine(target_state, buttons, joltages, lights_width=width, serial=serial))
    return machines


def bfs(buttons: list[int], target_state: int) -> list[int] | None:
    q = deque([(0, [])])  # path of length one for each button
    while q:
        state, path = q.popleft()
        if state == target_state:
            return path
        for b in buttons:
            next_state = state ^ b
            q.append((next_state, path + [b]))
    return None


def solve_part1(machines: list[Machine]) -> int:
    answer = 0
    for machine in machines:
        path = bfs(machine.buttons, machine.target_state)
        answer += len(path)
        print("serial", machine.serial, "target_state", machine.target_state, "path", path)
    return answer


def solve_part2(machines: list[Machine]) -> int:
    return -1


def main() -> None:
    ex_machines = parse(example[0])
    if solve_part1(ex_machines) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = parse(Path(__file__).with_suffix(".txt").read_text())

    start = time.perf_counter()
    answer = solve_part1(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(ex_machines) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(puzzle_input)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
