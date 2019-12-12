#!/usr/bin/env python

from collections import defaultdict
import copy
import math


class Moon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

    def __repr__(self):
        return f"[Moon {self.x},{self.y},{self.z} | vel {self.x_vel},{self.y_vel},{self.z_vel}]"

    def __str__(self):
        return f"[Moon {self.x},{self.y},{self.z} | vel {self.x_vel},{self.y_vel},{self.z_vel}]"


def test_input():
    return [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]


def test_input2():
    return [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]


def real_input():
    return [Moon(5, 4, 4), Moon(-11, -11, -3), Moon(0, 7, 0), Moon(-13, 2, 10)]


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


def energy(moon):
    potential = abs(moon.x) + abs(moon.y) + abs(moon.z)
    kinetic = abs(moon.x_vel) + abs(moon.y_vel) + abs(moon.z_vel)
    return potential * kinetic


def cycle_time(moons_in):
    moons = copy.deepcopy(moons_in)

    seen_x = defaultdict(int)
    seen_y = defaultdict(int)
    seen_z = defaultdict(int)

    h_x = hash_x(moons)
    seen_x[h_x] += 1

    h_y = hash_y(moons)
    seen_y[h_y] += 1

    h_z = hash_z(moons)
    seen_z[h_z] += 1

    seen_x_index = 0
    seen_y_index = 0
    seen_z_index = 0

    for i in range(100_000_000):
        moons = step(moons)

        h_x = hash_x(moons)
        h_y = hash_y(moons)
        h_z = hash_z(moons)

        if seen_x[h_x] > 0 and seen_x_index == 0:
            # print(f"x Seen before.. {i+1}")
            seen_x_index = i + 1

        if seen_y[h_y] > 0 and seen_y_index == 0:
            # print(f"y Seen before.. {i+1}")
            y_tripped = True
            seen_y_index = i + 1

        if seen_z[h_z] > 0 and seen_z_index == 0:
            # print(f"z Seen before.. {i+1}")
            z_tripped = True
            seen_z_index = i + 1

        if seen_x_index > 0 and seen_y_index > 0 and seen_z_index > 0:
            break

        seen_x[h_x] += 1
        seen_x[h_y] += 1
        seen_x[h_z] += 1

    return lcm(lcm(seen_x_index, seen_y_index), seen_z_index)


def energy_after_steps(moons_in, steps):
    moons = copy.deepcopy(moons_in)
    for i in range(steps):
        moons = step(moons)
    return total_energy(moons)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


if __name__ == "__main__":
    print("Part 1:")
    print(energy_after_steps(real_input(), 1000))

    print("Part 2:")
    print(cycle_time(real_input()))
