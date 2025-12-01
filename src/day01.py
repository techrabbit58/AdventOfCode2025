from pathlib import Path

example = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 3, 6

FULL_CIRCLE = 100  # 0 to 99


def parse(puzzle_input: str) -> list[int]:
    return [
        (int(rot[1:]) if rot[0] == "R" else (-int(rot[1:])))
        for rot in puzzle_input.split()
    ]


def solve(rotations: list[int]) -> tuple[int, int]:
    dial = 50
    zero_count = zero_transits = 0
    for rotation in rotations:
        # prepare for this step, both parts
        magnitude = abs(rotation)
        sign = rotation // magnitude
        new_dial = dial + sign * magnitude % FULL_CIRCLE  # skip extra circles

        # part 2 - count all zero transits
        zero_transits += magnitude // FULL_CIRCLE  # count extra circles
        # ... and now check if there is one final zero transit
        if dial != 0 and rotation > 0 and new_dial > FULL_CIRCLE:  # count zero visits for R
            zero_transits += 1  # case: add to non-null with carry
        elif dial != 0 and rotation < 0 and new_dial < FULL_CIRCLE:  # count zero visits for L
            zero_transits += 1  # case: subtract from non-null without carry
        elif new_dial == FULL_CIRCLE:  # count direct zero hits by L or R
            zero_transits += 1  # case: add or subtract with result being exactly null

        # part 1
        dial = new_dial % FULL_CIRCLE
        if dial == 0:
            zero_count += 1
    return zero_count, zero_transits


def main(puzzle_input: str) -> None:
    rotations = parse(example[0])
    part1test, part2test = solve(rotations)

    rotations = parse(Path(puzzle_input).read_text())
    part1solution, part2solution = solve(rotations)

    if part1test == example[1]:
        print("Part 1 solution:", part1solution)
    if part2test == example[2]:
        print("Part 2 solution:", part2solution)


if __name__ == "__main__":
    main("day01.txt")
