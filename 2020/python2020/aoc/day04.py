#!/usr/bin/env python
"""
Advent Of Code 2020 Day 4
https://adventofcode.com/2020/day/4
"""

import re

re_four_digits = r"^\d{4}$"
re_height = r"^(\d+)(cm|in)$"
re_hair = r"^#[a-f0-9]{6}$"
re_eye = r"^(amb|blu|brn|gry|grn|hzl|oth)$"
re_pid = r"^\d{9}$"


def is_valid_height(text):
    matches = re.match(re_height, text)
    if not matches:
        return False
    if matches[2] == "in":
        return 59 <= int(matches[1]) <= 76
    if matches[2] == "cm":
        return 150 <= int(matches[1]) <= 193
    return False


required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
rules = {
    "byr": lambda x: re.match(re_four_digits, x) and (1920 <= int(x) <= 2002),
    "iyr": lambda x: re.match(re_four_digits, x) and (2010 <= int(x) <= 2020),
    "eyr": lambda x: re.match(re_four_digits, x) and (2020 <= int(x) <= 2030),
    "hgt": is_valid_height,
    "hcl": lambda x: re.match(re_hair, x),
    "ecl": lambda x: re.match(re_eye, x),
    "pid": lambda x: re.match(re_pid, x),
}


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        passports = lines.split("\n\n")
        return [parse_passport(x) for x in passports]


def parse_passport(raw_passport):
    pairs = re.split(r"\s+", raw_passport)
    fields = []
    for pair in pairs:
        field, val = pair.split(":")
        fields.append((field, val))
    return fields


def is_valid_passport1(passport):
    fields_seen = [pair[0] for pair in passport]
    missing = set(required) - set(fields_seen)
    return len(missing) == 0


def is_valid_passport2(passport):
    if not is_valid_passport1(passport):
        return False
    for (field, val) in passport:
        if field not in rules:
            continue
        if not rules[field](val):
            return False
    return True


class Day04:
    """ AoC 2020 Day 04 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 1 """
        passports = parse(filename)
        valid_passports = [
            passport for passport in passports if is_valid_passport1(passport)
        ]
        return len(valid_passports)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 04 part 2 """
        passports = parse(filename)
        valid_passports = [
            passport for passport in passports if is_valid_passport2(passport)
        ]
        return len(valid_passports)
