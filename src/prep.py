"""
Prepare for a new day of AoC 2025.
(1) Create a dayNN.py file for the code.
(2) Download puzzle input and create a dayNN.txt file.
"""
import argparse
import os
from pathlib import Path
from string import Template

import requests
from dotenv import load_dotenv

YEAR = 2025

template = Template('''"""
AdventOfCode $year Day $day
https://adventofcode.com/$year/day/$day
"""
import time
from pathlib import Path

example = """""", None, None


def parse(text: str):
    ...


def solve_part1(puzzle_input) -> int:
    ...


def solve_part2(puzzle_input) -> int:
    ...


def main() -> None:
    if solve_part1(example[0]) != example[1]:
        print("Part 1 not done")
        exit()

    puzzle_input = Path(__file__).with_suffix(".txt").read_text()

    start = time.perf_counter()
    answer = solve_part1(puzzle_input)
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve_part2(example[0]) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve_part2(puzzle_input)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
''')

url_template = Template('https://adventofcode.com/$year/day/$day/input')


load_dotenv()


def download(url: str) -> str | None:
    headers = {"Cookie": os.environ.get("ADVENT_OF_CODE")}
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(response.status_code, response.reason)
        return None
    else:
        return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare for a new day of AoC (1...12).")
    parser.add_argument("day", metavar="DAY", type=int, choices=range(1, 13))
    parser.add_argument(
        "-d", "--download",
        action="store_true",
        default=False,
        help="option flag: if set, get your puzzle input (default=not set)")
    args = parser.parse_args()

    prog = Path(f"day{args.day:02d}.py")

    if prog.exists():
        print(f"File exists: {prog.as_posix()}, did not overwrite")
    else:
        prog.write_text(template.substitute(day=args.day, year=YEAR))
        print(f"New file: {prog.as_posix()}")

    data = prog.with_suffix(".txt")

    if data.exists():
        print(f"File exists: {data.as_posix()}, did not overwrite")
    else:
        if args.download:
            text = download(url_template.substitute(day=args.day, year=YEAR))
        else:
            text = ""
        if text and text != "":
            data.write_text(text)
            print(f"New file: {data.as_posix()}")
        elif text is None:
            print(f"No new file: {data.as_posix()}, input is not yet available.")
            print(f"Do not try again before day {args.day}. This is pointless.")
        else:
            print(f"No new file: {data.as_posix()}, use --download to get it.")


if __name__ == "__main__":
    main()
