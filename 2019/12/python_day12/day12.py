#!/usr/bin/env python
import hashlib

from itertools import permutations
from collections import defaultdict


class Moon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

    def __repr__(self):
        return f"[Moon {self.x},{self.y},{self.z} | velocity {self.x_vel},{self.y_vel},{self.z_vel}]"

    def __str__(self):
        return f"[Moon {self.x},{self.y},{self.z} | velocity {self.x_vel},{self.y_vel},{self.z_vel}]"


def test_input():
    moons = [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]
    return moons


def test_input2():
    moons = [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]
    return moons


def real_input():
    moons = [Moon(5, 4, 4), Moon(-11, -11, -3), Moon(0, 7, 0), Moon(-13, 2, 10)]
    return moons


def step(moons):
    for i, moon_i in enumerate(moons):
        for j, moon_j in enumerate(moons):
            if i >= j:
                continue
            if moon_i.x > moon_j.x:
                moon_i.x_vel -= 1
                moon_j.x_vel += 1
            elif moon_i.x < moon_j.x:
                moon_i.x_vel += 1
                moon_j.x_vel -= 1
            if moon_i.y > moon_j.y:
                moon_i.y_vel -= 1
                moon_j.y_vel += 1
            elif moon_i.y < moon_j.y:
                moon_i.y_vel += 1
                moon_j.y_vel -= 1
            if moon_i.z > moon_j.z:
                moon_i.z_vel -= 1
                moon_j.z_vel += 1
            elif moon_i.z < moon_j.z:
                moon_i.z_vel += 1
                moon_j.z_vel -= 1
            # print(f"pair {i} {j}")

    for i, moon_i in enumerate(moons):
        moon_i.x += moon_i.x_vel
        moon_i.y += moon_i.y_vel
        moon_i.z += moon_i.z_vel
    return moons


def total_energy(moons):
    return sum(energy(moon) for moon in moons)


def hash_y(moons):
    tup = (
        moons[0].y,
        moons[0].y_vel,
        moons[1].y,
        moons[1].y_vel,
        moons[2].y,
        moons[2].y_vel,
        moons[3].y,
        moons[3].y_vel,
    )
    return tup


def hash_z(moons):
    tup = (
        moons[0].z,
        moons[0].z_vel,
        moons[1].z,
        moons[1].z_vel,
        moons[2].z,
        moons[2].z_vel,
        moons[3].z,
        moons[3].z_vel,
    )
    return tup


def hash_x(moons):
    tup = (
        moons[0].x,
        moons[0].x_vel,
        moons[1].x,
        moons[1].x_vel,
        moons[2].x,
        moons[2].x_vel,
        moons[3].x,
        moons[3].x_vel,
    )
    return tup


def hash_moons(moons):
    tup = (
        moons[0].x
        + moons[0].y * 2
        + moons[0].z * 4
        + moons[0].x_vel * 8
        + moons[0].y_vel * 16
        + moons[0].z_vel * 32,
        moons[1].x
        + moons[1].y * 2
        + moons[1].z * 4
        + moons[1].x_vel * 8
        + moons[1].y_vel * 16
        + moons[1].z_vel * 32,
        moons[2].x
        + moons[2].y * 2
        + moons[2].z * 4
        + moons[2].x_vel * 8
        + moons[2].y_vel * 16
        + moons[2].z_vel * 32,
        moons[3].x
        + moons[3].y * 2
        + moons[3].z * 4
        + moons[3].x_vel * 8
        + moons[3].y_vel * 16
        + moons[3].z_vel * 32,
        total_energy(moons),
    )
    return tup


def energy(moon):
    potential = abs(moon.x) + abs(moon.y) + abs(moon.z)
    kinetic = abs(moon.x_vel) + abs(moon.y_vel) + abs(moon.z_vel)
    return potential * kinetic


def double_check(moons, range_max):
    seen_x = defaultdict(int)
    seen_y = defaultdict(int)
    seen_z = defaultdict(int)

    h_x = hash_x(moons)
    seen_x[h_x] += 1

    h_y = hash_y(moons)
    seen_y[h_y] += 1

    h_z = hash_z(moons)
    seen_z[h_z] += 1

    x_tripped = False
    y_tripped = False
    z_tripped = False

    for i in range(range_max):
        moons = step(moons)

        h_x = hash_x(moons)
        h_y = hash_y(moons)
        h_z = hash_z(moons)

        if seen_x[h_x] > 0 and (not x_tripped):
            print(f"x Seen before.. {i+1}")
            x_tripped = True

        if seen_y[h_y] > 0 and (not y_tripped):
            print(f"y Seen before.. {i+1}")
            y_tripped = True

        if seen_z[h_z] > 0 and (not z_tripped):
            print(f"z Seen before.. {i+1}")
            z_tripped = True

        seen_x[h_x] += 1
        seen_x[h_y] += 1
        seen_x[h_z] += 1


if __name__ == "__main__":
    # moons = test_input()
    # for i in range(10):
    #     moons = step(moons)
    # print(moons)
    # print(total_energy(moons))

    # moons = real_input()
    # for i in range(1000):
    #     moons = step(moons)
    # print(moons)

    ##### REAL
    moons = test_input()
    seen = defaultdict(int)
    h = hash_moons(moons)
    print(h)
    seen[h] += 1
    for i in range(568677492400):
        moons = step(moons)
        h = hash_moons(moons)
        if seen[h] > 0:
            print(f"Seen before.. i #{i+1}")
            print(moons)
            break
        seen[h] += 1
        if i % 100000 == 0:
            print(i)

    double_check(real_input(), 1000000)

    ##### REAL
    # moons = real_input()
    # seen = defaultdict(int)
    # h = hash_moons(moons)
    # print(h)
    # seen[h] += 1
    # for i in range(568677492400):
    #     moons = step(moons)
    #     h = hash_moons(moons)
    #     if seen[h] > 0:
    #         print(f"Seen before.. i #{i+1}")
    #         print(moons)
    #         break
    #     seen[h] += 1
    #     if i % 100000 == 0:
    #         print(i)

    # print(moons)
    # print(hash_moons(moons))
    # print(total_energy(moons))
    # program = parse("../../11/input.txt")
    # print(part1(program))
    # print("Part 2:")
    # print(part2(program))
