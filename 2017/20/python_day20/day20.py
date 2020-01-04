#!/usr/bin/env python
import re
import operator
from functools import reduce
from collections import defaultdict


def flatten(a_list):
    return reduce(operator.add, a_list, [])


def parse(filename):
    with open(filename) as file:
        particles = [parse_line(line) for line in file]
        return Group(particles)


def parse_line(line):
    px, py, pz = re.search(r"p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>", line).groups()
    vx, vy, vz = re.search(r"v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>", line).groups()
    ax, ay, az = re.search(r"a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>", line).groups()
    pos = Point(px, py, pz)
    vel = Point(vx, vy, vz)
    acc = Point(ax, ay, az)
    return Particle(pos, vel, acc)


class Point:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f"<Point {self.x}, {self.y}, {self.z}>"

    def to_tuple(self):
        return (self.x, self.y, self.z)


class Particle:
    def __init__(self, pos, vel, acc):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def __repr__(self):
        return f"<Particle pos #{self.pos}, vel #{self.vel}, acc #{self.acc} = dist {self.distance}>"

    @property
    def distance(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def step(self):
        # Increase velocity by acceleration
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        self.vel.z += self.acc.z

        # Increase position by velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def is_same_sign(self):
        x = (self.pos.x >= 0 and self.vel.x >= 0 and self.acc.x >= 0) or (
            self.pos.x <= 0 and self.vel.x <= 0 and self.acc.x <= 0
        )
        y = (self.pos.y >= 0 and self.vel.y >= 0 and self.acc.y >= 0) or (
            self.pos.y <= 0 and self.vel.y <= 0 and self.acc.y <= 0
        )
        z = (self.pos.z >= 0 and self.vel.z >= 0 and self.acc.z >= 0) or (
            self.pos.z <= 0 and self.vel.z <= 0 and self.acc.z <= 0
        )
        return x and y and z


class Group:
    """ A group of particles """

    def __init__(self, particles):
        self.particles = particles

    def __len__(self):
        return len(self.particles)

    def display(self):
        """ Print to screen """
        for particle in self.particles:
            print(particle)
        print(f"Min: #{self.min()}")
        print(f"All same sign: #{self.all_same_sign()}")
        print("")

    def all_same_sign(self):
        return all(p.is_same_sign() for p in self.particles)

    def step(self):
        for particle in self.particles:
            particle.step()

    def step_with_collide(self):
        self.step()
        self.remove_collide()

    def remove_collide(self):
        locs_seen = defaultdict(lambda: 0)
        index_of_loc = defaultdict(list)

        # Count how many times we've seen each location (store a list of particle indexes matching each location)
        for i, particle in enumerate(self.particles):
            loc = particle.pos.to_tuple()
            locs_seen[loc] += 1
            index_of_loc[loc].append(i)

        # Compute which indexes in the list to remove
        locs_to_remove = [loc for loc, count in locs_seen.items() if count > 1]
        idx_to_remove = flatten([index_of_loc[loc] for loc in locs_to_remove])

        # Remove the indexes in backward order (so any deletion doesn't change other indicies)
        for i in sorted(idx_to_remove, reverse=True):
            del self.particles[i]

    def min(self):
        min_index, min_value = min(
            enumerate(self.particles), key=lambda x: x[1].distance
        )
        return min_index


if __name__ == "__main__":
    # Part 1
    data = parse("../input.txt")
    while not data.all_same_sign():
        data.step()
    for i in range(10):
        data.step()
    print("Part 1:")
    print(data.min())

    # Part 2
    data = parse("../input.txt")
    while not data.all_same_sign():
        data.step_with_collide()
    for i in range(10):
        data.step_with_collide()
    print("Part 2:")
    print(len(data))
