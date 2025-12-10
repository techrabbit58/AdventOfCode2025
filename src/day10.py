"""
AdventOfCode 2025 Day 10
https://adventofcode.com/2025/day/10
"""
import re
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
    wiring: list[tuple[int, ...]]
    joltages: list[int]
    lights_width: int = field(repr=False, kw_only=True)


def parse(text: str) -> list[Machine]:
    machines = []
    for serial, line in enumerate(text.splitlines(), 1):
        target_state = 0
        width = 0
        for i, c in enumerate(re.search(r"\[(?P<ind>[.#]+),?]", line).group("ind")):
            if c == "#":
                target_state |= 1 << i
            width = i
        width += 1
        buttons = []
        wiring = []
        for button in re.findall(r"(\(.+?\))", line):
            wires = 0
            plugs = tuple(map(int, re.findall(r"(\d+)", button)))
            for n in plugs:
                wires |= 1 << n
            buttons.append(wires)
            wiring.append(plugs)
        joltages = [int(n) for n in re.search(r"\{(?P<jol>(\d+,?)+)}", line).group("jol").split(",")]
        machines.append(Machine(target_state, buttons, wiring, joltages, lights_width=width, serial=serial))
    return machines


def lights_bfs(buttons: list[int], target_state: int) -> list[int] | None:
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
        path = lights_bfs(machine.buttons, machine.target_state)
        answer += len(path)
        print("serial", machine.serial, "target_state", machine.target_state, "path", path)
    print("-" * 72)
    return answer


def all_zero(joltages: list[int]) -> bool:
    return all(map(lambda x: x == 0, joltages))


def apply(wires: tuple[int, ...], joltages: list[int]) -> list[int]:
    new_joltages = joltages.copy()
    for wire in wires:
        new_joltages[wire] -= 1
    return new_joltages


def is_negative(joltages: list[int]) -> bool:
    return any(map(lambda x: x < 0, joltages))


def joltage_bfs(wirings: list[tuple[int, ...]], target_joltages: list[int]) -> list[int] | None:
    q = deque([(target_joltages, [])])  # path of length one for each button
    last_length = 0
    while q:
        joltages, path = q.popleft()
        if (new_length := len(path)) > last_length:
            last_length = new_length
            print("path length", last_length)
        if all_zero(joltages):
            return path
        for w in wirings:
            next_joltages = apply(w, joltages)
            if is_negative(next_joltages):
                continue
            q.append((next_joltages, path + [w]))
    return None


def solve_part2(machines: list[Machine]) -> int:
    answer = 0
    for machine in machines:
        path = joltage_bfs(machine.wiring, machine.joltages)
        answer += len(path)
        print("serial", machine.serial, "target_state", machine.target_state, "pathlen", len(path))
    print("-" * 72)
    return answer


def main() -> None:
    ex_machines = parse(example[0])
    if solve_part1(ex_machines) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = parse(Path(__file__).with_suffix(".txt").read_text())

    part1_start = time.perf_counter()
    part1_answer = solve_part1(puzzle_input)
    part1_end = time.perf_counter()
    print(f"Part 1 solution: {part1_answer}, runtime = {part1_end - part1_start:.3f} s")
    print("=" * 72)

    if solve_part2(ex_machines) != example[2]:
        print("Part 2 not done")
        exit()

    part2_start = time.perf_counter()
    part2_answer = solve_part2(puzzle_input)
    part2_end = time.perf_counter()
    # print(f"Part 1 solution: {part1_answer}, runtime = {part1_end - part1_start:.3f} s")
    print(f"Part 2 solution: {part2_answer}, runtime = {part2_end - part2_start:.3f} s")


if __name__ == "__main__":
    main()
