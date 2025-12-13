"""
AdventOfCode 2025 Day 10
https://adventofcode.com/2025/day/10
"""
import configparser
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import z3


@dataclass(kw_only=True)
class Machine:
    serial: int
    target_state: int
    buttons: list[int]
    wiring: list[list[int]]
    joltages: list[int]


def parse(text: str) -> list[Machine]:
    machines = []
    for serial, line in enumerate(text.splitlines(), 1):
        lights, *buttons, joltages = line.split()
        button_values = []
        wiring = []
        for button in buttons:
            wiring.append(list(map(int, button.strip("()").split(","))))
            button_values.append(sum(2 ** b for b in wiring[-1]))
        machines.append(Machine(
            serial=serial,
            target_state=int(lights.strip("[]")[::-1].replace("#", "1").replace(".", "0"), 2),
            buttons=button_values,
            wiring=wiring,
            joltages=list(map(int, joltages.strip("{}").split(",")))
        ))
    return machines


def solve_part1(machines: list[Machine]) -> int:
    answer = 0

    for machine in machines:
        buttons = machine.buttons
        target_state = machine.target_state
        min_presses = None

        # with XOR, pressing a button once is sufficient (because even numbers of
        # presses are as good as never and every uneven number of presses is
        # as good as pressing a button only once)
        for i in range(1, len(buttons)):  # each button shall be pressed at least once
            for seq in combinations(buttons, i):  # simulates bfs, but without repetitions
                result = 0
                for button in seq:
                    result ^= button
                if result == target_state:
                    min_presses = i
                    break
            if min_presses is not None:
                break

        answer += min_presses

    return answer


def solve_part2(machines: list[Machine]) -> int:
    """
    Again, part 2 was way too hard for me. I needed help.
    This genius part 2 solution, I've borrowed it from YT "0xdf".

    Watch his video to see the shiny and quick solution that is based
    on a magic thing called "z3-solver". This is an extra library,
    and not part of python's standard library.
    Use "pip install z3-solver" or "uv add z3-solver" or else before
    you can use the solver.

    I'm not familiar with this kind of optimization problems and
    never came across such a "Z3 solver". It's completely new to me.

    It looks as if the solver is kind of a LISP-driven thing,
    and there are LISP programs generated and executed inside the solver
    instance. The optimization process seems to be always the same,
    but during setup one defines input variables, output variables
    and goals. The solver then spits out an optimization result that
    must be translated back to python values.

    I suggest you consider subscribing to 0xdf's YT channel or,
    at least, give his day 10 video a like.
    """
    answer = 0

    for machine in machines:
        buttons = machine.wiring
        targets = machine.joltages

        opt = z3.Optimize()  # this is where the black wizardry takes over, we light a fire under the cauldron

        x = [z3.Int(f"x{i}") for i in range(len(buttons))]  # make x a list of optimization variables

        for xi in x:
            opt.add(xi >= 0)  # ... and give this to the optimizer as a first constraint

        for i, target in enumerate(targets):  # make a list of optimization variables
            coef = [int(i in button) for button in buttons]  # first make a list of coefficients
            opt.add(z3.Sum(c * xi for c, xi in zip(coef, x)) == target)  # and then add it as optimizer goals

        opt.minimize(z3.Sum(x))  # let the cauldron boil it

        if opt.check() == z3.sat:  # if the position has the right color and smell
            m = opt.model()  # ... let's take a sip of the potion, we can now see the answer for this machine
            answer += sum(m[xi].as_long() for xi in x)  # add all answers up

    return answer


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

    ex_machines = parse(example[0])
    if solve_part1(ex_machines) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = parse(Path(__file__).with_suffix(".txt").read_text())

    part1_start = time.perf_counter()
    part1_answer = solve_part1(puzzle_input)
    part1_end = time.perf_counter()
    print(f"Part 1 solution: {part1_answer}, runtime = {part1_end - part1_start:.3f} s")

    if solve_part2(ex_machines) != example[2]:
        print("Part 2 not done")
        exit()

    part2_start = time.perf_counter()
    part2_answer = solve_part2(puzzle_input)
    part2_end = time.perf_counter()
    print(f"Part 2 solution: {part2_answer}, runtime = {part2_end - part2_start:.3f} s")


if __name__ == "__main__":
    main()
