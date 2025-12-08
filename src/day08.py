"""
AdventOfCode 2025 Day 8
https://adventofcode.com/2025/day/8
"""
import math
import time
from collections import deque
from itertools import combinations
from pathlib import Path

example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""", 40, 25272

type Vector = tuple[int, int, int]  # v = (x, y, z)
type Circuit = set[Vector]


def parse(text: str) -> set[Vector]:
    vectors = set()
    for line in text.splitlines():
        vectors.add(tuple(map(int, line.split(","))))
    return vectors


def squared_distance(p: Vector, q: Vector) -> int:
    return abs(p[0] - q[0]) ** 2 + abs(p[1] - q[1]) ** 2 + abs(p[2] - q[2]) ** 2


def solve(vectors: set[Vector], limit: int = None) -> int:
    nodes = {
        squared_distance(p, q): {p, q}
        for p, q in combinations(vectors, 2)
    }

    connection_cost = sorted(nodes.keys())
    circuits = deque()
    circuits.append(nodes[connection_cost[0]])
    last_seen = list(circuits[0])
    singles = vectors.copy()

    for i, cost in enumerate(connection_cost[1:], 1):
        if i == limit or not singles:  # limit: part 1, singles: part 2
            break

        connection = nodes[cost]
        singles -= connection  # part 2
        last_seen = list(connection)  # part 2

        # step 1: add new connection to existing circuit or add as new subcircuit
        for circuit in circuits:
            if circuit & connection:
                circuit |= connection
                break
        else:
            circuits.append(connection)

        # step 2: connect subcircuits
        for c1, c2 in combinations(circuits, 2):
            if c1 & c2:
                connected_circuit = c1 | c2
                circuits.remove(c1)
                circuits.remove(c2)
                circuits.append(connected_circuit)

    # part 1:
    # add vectors that are still unconnected
    # just to be sure to catch all circuits for part 1,
    # due to a remark in the explanation of AoCs part 1 example
    for single in singles:
        circuits.append({single})

    circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)

    if limit is None:  # part 2
        (x1, _, _), (x2, _, _) = last_seen
        answer = x1 * x2
    else:  # part 1
        answer = math.prod(circuit_sizes[:3])

    return answer


def main() -> None:
    ex_vectors = parse(example[0])

    if solve(ex_vectors, 10) != example[1]:
        print("Part 1 not done")
        exit()

    vectors = parse(Path(__file__).with_suffix(".txt").read_text())

    start = time.perf_counter()
    answer = solve(vectors, len(vectors))
    end = time.perf_counter()
    print(f"Part 1 solution: {answer}, runtime = {end - start:.3f} s")

    if solve(ex_vectors) != example[2]:
        print("Part 2 not done")
        exit()

    start = time.perf_counter()
    answer = solve(vectors)
    end = time.perf_counter()
    print(f"Part 2 solution: {answer}, runtime = {end - start:.3f} s")


if __name__ == "__main__":
    main()
