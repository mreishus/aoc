#!/usr/bin/env python
import math
import numpy as np


def allrots(m):
    """ All rotations of a matrix """
    yield m
    yield np.rot90(m, k=1)
    yield np.rot90(m, k=2)
    yield np.rot90(m, k=3)


def all_rots_and_flips(m):
    """ All flips + rotations of a matrix """
    yield from allrots(m)
    yield from allrots(np.flipud(m))
    yield from allrots(np.fliplr(m))


# Blockshaped / Unblockshaped from StackOverflow
def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array looks like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (
        arr.reshape(h // nrows, nrows, -1, ncols)
        .swapaxes(1, 2)
        .reshape(-1, nrows, ncols)
    )


def unblockshaped(arr, h, w):
    """
    Return an array of shape (h, w) where
    h * w = arr.size

    If arr is of shape (n, nrows, ncols), n sublocks of shape (nrows, ncols),
    then the returned array preserves the "physical" layout of the sublocks.
    """
    n, nrows, ncols = arr.shape
    return arr.reshape(h // nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(h, w)


class Grid:
    def __init__(self, filename):
        self.grid = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
        self.rules = None
        self.load_rules(filename)

    def load_rules(self, filename):
        self.rules = {}
        with open(filename) as file:
            for line in file:
                left, right = line.strip().split(" => ")
                left = self.str_to_matrix(left)
                right = self.str_to_matrix(right)

                for m in all_rots_and_flips(left):
                    self.rules[m.tobytes()] = right

    def str_to_matrix(self, string):
        rows = []
        for row_str in string.split("/"):
            row = np.array([1 if c == "#" else 0 for c in row_str])
            rows.append(row)
        return np.array(rows)

    def step(self):
        size_x, size_y = self.grid.shape
        if size_x != size_y:
            raise ValueError("Non-square grid")
        if size_x % 2 == 0:
            self.step2()
        elif size_x % 3 == 0:
            self.step3()
        else:
            raise ValueError("Don't know what rule to apply")

    def subgrids_to_square(self, subgrids):
        s = int(math.sqrt(subgrids.size))
        return unblockshaped(subgrids, s, s)

    def step2(self):
        # Split into 2x2 subgrids, Check how many made
        subgrids = blockshaped(self.grid, 2, 2)
        (num_sub, _, _) = subgrids.shape

        # Output is same # of 3x3 subgrids
        newgrid = np.zeros((num_sub, 3, 3), dtype=int)
        for i in range(num_sub):
            newgrid[i] = self.rules[subgrids[i].tobytes()]

        # Join together subgrids
        self.grid = self.subgrids_to_square(newgrid)

    def step3(self):
        # Split into 3x3 subgrids, Check how many made
        subgrids = blockshaped(self.grid, 3, 3)
        (num_sub, _, _) = subgrids.shape

        # Output is same # of 4x4 subgrids
        newgrid = np.zeros((num_sub, 4, 4), dtype=int)
        for i in range(num_sub):
            newgrid[i] = self.rules[subgrids[i].tobytes()]

        # Join together subgrids
        self.grid = self.subgrids_to_square(newgrid)

    def num_on(self):
        return self.grid[self.grid == 1].size


if __name__ == "__main__":
    print("Part 1:")
    g = Grid("../input.txt")
    for i in range(5):
        g.step()
    print(g.num_on())

    print("Part 2:")
    g = Grid("../input.txt")
    for i in range(18):
        g.step()
    print(g.num_on())
