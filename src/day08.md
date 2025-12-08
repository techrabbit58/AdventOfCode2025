# Kruskal's Algorithm
My solution is not very efficient. It is home-grown, and kind of "naive".

I'd better known [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
before starting the solution. Because I didn't, I hat to find an own algorithm.

It turns out, mine works, but is unnecessarily slow.

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

    print("\n--- result ---")
    print("edges of MST:", mst)  # MST = Minimum Spanning Tree
    print("total cost:", total_cost)
```

It produces output like so:
```
Kante hinzugefügt: 0 -- 1 (Kosten: 1)
Kante hinzugefügt: 1 -- 2 (Kosten: 2)
Kante hinzugefügt: 2 -- 3 (Kosten: 3)
Kante hinzugefügt: 3 -- 4 (Kosten: 4)
Kante hinzugefügt: 4 -- 5 (Kosten: 5)
Kante hinzugefügt: 5 -- 6 (Kosten: 6)
Kante hinzugefügt: 6 -- 7 (Kosten: 7)
Kante hinzugefügt: 7 -- 8 (Kosten: 8)
Kante hinzugefügt: 8 -- 9 (Kosten: 9)

--- Ergebnis ---
MST-Kanten: [(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 4, 4), (4, 5, 5),
             (5, 6, 6), (6, 7, 7), (7, 8, 8), (8, 9, 9)]
Gesamtkosten: 45
```
---
