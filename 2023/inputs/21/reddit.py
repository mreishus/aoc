#!/bin/python3
inp = ""
with open("input.txt") as f:
    inp = f.read().strip()
grid = list(map(list, inp.split("\n")))

dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

n = len(grid)
m = len(grid[0])
print(n, m)

q = set()
for i in range(n):
    for j in range(m):
        if grid[i][j] == "S":
            q.add((i, j))

goal = 26501365


def f(n):
    a0 = 3906
    a1 = 34896
    a2 = 96784

    b0 = a0
    b1 = a1 - a0
    b2 = a2 - a1
    return b0 + b1 * n + (n * (n - 1) // 2) * (b2 - b1)


print(f(goal // n))

plen = 0
for itt in range(1, 100000):
    nq = set()
    for i, j in q:
        for k in range(4):
            ni = i + dx[k]
            nj = j + dy[k]
            if grid[ni % n][nj % m] != "#":
                nq.add((ni, nj))
    q = nq
    if itt % n == goal % n:
        print(itt, len(q), len(q) - plen, itt // n)
        plen = len(q)

print(len(q))
