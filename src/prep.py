"""
Prepare for a new day of AoC.
(1) Create a dayNN.py file for the code.
(2) Create a dayNN.txt file for the puzzle input text.
"""
import argparse
import os
from pathlib import Path
from string import Template

import requests
from dotenv import load_dotenv

template = Template('''"""
AdventOfCode 2025 Day $day
"""
from pathlib import Path

example = """
"""


def solve() -> int:
    ...


def main() -> None:
    puzzle_input = Path(__file__).with_suffix(".txt").read_text()
    print(puzzle_input)


if __name__ == "__main__":
    main()
''')

url_template = Template('https://adventofcode.com/2025/day/$day/input')

load_dotenv()
print(os.environ.get("ADVENT_OF_CODE"))


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
    args = parser.parse_args()
    prog = Path(f"day{args.day:02d}.py")
    if prog.exists():
        print(f"File exists: {prog.as_posix()}, did not overwrite")
    else:
        prog.write_text(template.substitute(day=args.day))
        print(f"New file: {prog.as_posix()}")
    data = prog.with_suffix(".txt")
    if data.exists():
        print(f"File exists: {data.as_posix()}, did not overwrite")
    else:
        text = download(url_template.substitute(day=args.day))
        if text:
            data.write_text(text)
            print(f"New file: {data.as_posix()}")
        else:
            print(f"No new file: {data.as_posix()}, input is not yet available.")
            print(f"Do not try again before day {args.day}. This is pointless.")


if __name__ == "__main__":
    main()
