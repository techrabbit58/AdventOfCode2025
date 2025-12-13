# Kruskal's Algorithm
My solution is not very efficient. It is home-grown, and kind of "naive".

I'd better known [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
before starting the solution. Because I didn't, I hat to find an own algorithm.

It turns out, mine works, but is needlessly slow.

Here is an example of Kruskal's algorithm:

```python3
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Pfadkompression
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False  # Zyklus würde entstehen
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


def kruskal(n, edges):
    """
    n: number of nodes
    edges: list of (cost, u, v)
    """
    uf = UnionFind(n)
    mst = []
    total_cost = 0

    # Kanten nach Kosten sortieren
    edges.sort(key=lambda x: x[0])

    for cost, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, cost))
            total_cost += cost
            print(f"New edge: {u} -- {v} (cost: {cost})")
        if len(mst) == n - 1:
            break

    return mst, total_cost


def main():
    # example: 10 random nodes, (cost, u, v), wher u and v are the nodes given by node ID
    edges = [
        (1, 0, 1), (2, 1, 2), (3, 2, 3), (4, 3, 4),
        (5, 4, 5), (6, 5, 6), (7, 6, 7), (8, 7, 8),
        (9, 8, 9), (10, 0, 9), (11, 2, 7), (12, 1, 8)
    ]

    mst, total_cost = kruskal(10, edges)

    print("\n--- Result ---")
    print("Edges of MST:", mst)  # MST = Minimum Spanning Tree
    print("Total cost:", total_cost)
```

It produces output like so:
```
New edge: 0 -- 1 (cost: 1)
New edge: 1 -- 2 (cost: 2)
New edge: 2 -- 3 (cost: 3)
New edge: 3 -- 4 (cost: 4)
New edge: 4 -- 5 (cost: 5)
New edge: 5 -- 6 (cost: 6)
New edge: 6 -- 7 (cost: 7)
New edge: 7 -- 8 (cost: 8)
New edge: 8 -- 9 (cost: 9)

--- Result ---
Edges of MST: [(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 4, 4), (4, 5, 5),
             (5, 6, 6), (6, 7, 7), (7, 8, 8), (8, 9, 9)]
Total cost: 45
```
---
