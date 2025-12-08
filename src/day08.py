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
type NodeId = int
type Circuit = set[NodeId]


def parse(text: str) -> set[Vector]:
    vectors = set()
    for line in text.splitlines():
        vectors.add(tuple(map(int, line.split(","))))
    return vectors


def squared_distance(p: Vector, q: Vector) -> int:
    return abs(p[0] - q[0]) ** 2 + abs(p[1] - q[1]) ** 2 + abs(p[2] - q[2]) ** 2


def solve(vectors: set[Vector], limit: int | None = None) -> int:
    """
    This solves part 1 if the limit is set.
    This solves part 2 if the limit is not set.
    """
    nodes = {i: j for i, j in enumerate(vectors)}
    connection_by_cost = {
        squared_distance(p, q): {i, j}
        for (i, p), (j, q) in combinations(nodes.items(), 2)
    }
    ranks = sorted(connection_by_cost.keys())

    circuits = deque()
    circuits.append(connection_by_cost[ranks[0]])
    last_seen = list(circuits[0])
    singles = set(nodes.keys())

    for i, current_rank in enumerate(ranks[1:], 1):
        if i == limit or not singles:  # limit: part 1, singles: part 2
            break

        connection = connection_by_cost[current_rank]
        singles -= connection
        last_seen = list(connection)  # part 2

        connect(circuits, connection)
        merge(circuits)

    # part 1:
    # add vectors that are still unconnected
    # just to be sure to catch all circuits for part 1
    # (this is due to a remark in the explanation of AoCs part 1 example)
    for single in singles:
        circuits.append({single})

    circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)  # part 1
    part1 = math.prod(circuit_sizes[:3])

    n1, n2 = last_seen  # part 2
    part2 = nodes[n1][0] * nodes[n2][0]

    return part1 if limit is not None else part2


def merge(circuits: deque[Circuit]) -> None:
    for c1, c2 in combinations(circuits, 2):
        if c1 & c2:
            connected_circuit = c1 | c2
            circuits.remove(c1)
            circuits.remove(c2)
            circuits.append(connected_circuit)


def connect(circuits: deque[Circuit], new_pair: Circuit) -> None:
    for circuit in circuits:
        if circuit & new_pair:
            circuit |= new_pair
            break
    else:
        circuits.append(new_pair)


def main() -> None:
    ex_vectors = parse(example[0])
    ex_limit = 10

    if solve(ex_vectors, ex_limit) != example[1]:
        print("Part 1 not done")
        exit()

    vectors = parse(Path(__file__).with_suffix(".txt").read_text())
    limit = 1000

    start = time.perf_counter()
    answer = solve(vectors, limit)
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
