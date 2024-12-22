#!/usr/bin/env python
"""
Advent Of Code 2024 Day 09
https://adventofcode.com/2024/day/7
"""


class Range:
    def __init__(self, id, begin, end):
        self.id = id
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"#{self.id}[{self.begin}, {self.end}]"

    def __repr__(self):
        return self.__str__()


def parse(filename):
    with open(filename) as file:
        text = file.read().strip()

    disk = []
    is_data = True
    i = 0
    id = 0
    # text = "12345"
    for char in text:
        num = int(char)

        begin = i
        end = i + num - 1
        # print(num)
        if is_data and num > 0:
            r = Range(id, begin, end)
            id += 1
        elif num > 0:
            r = Range(".", begin, end)

        if num > 0:
            disk.append(r)

        i = end + 1
        is_data = not is_data
    return disk, id - 1


def checksum(disk):
    chk = 0
    i = 0
    range_ptr = 0
    while True:
        block = disk[range_ptr]
        finished = False
        while not (block.begin <= i <= block.end):
            if range_ptr + 1 >= len(disk):
                finished = True
                break
            range_ptr += 1
            block = disk[range_ptr]
        if finished:
            break

        if block.begin <= i <= block.end:
            if block.id != ".":
                chk += i * block.id
        i += 1
    return chk


def display(disk):
    i = 0
    range_ptr = 0
    while True:
        block = disk[range_ptr]
        finished = False
        while not (block.begin <= i <= block.end):
            if range_ptr + 1 >= len(disk):
                finished = True
                break
            range_ptr += 1
            block = disk[range_ptr]
        if finished:
            break

        if block.begin <= i <= block.end:
            print(block.id, end="")
        i += 1
    print("")


def consolidate_whole_files_method(disk, file_id):
    data_ptr = len(disk) - 1
    while file_id > 0:
        # Look for file from the right
        data_block = disk[data_ptr]
        while data_block.id != file_id:
            data_ptr -= 1
            data_block = disk[data_ptr]
        # print("Found file_id?", file_id, data_block)

        data_len = data_block.end - data_block.begin + 1
        # Start left and look for enough open space
        space_ptr = 0
        success = False
        while space_ptr <= len(disk) - 1 and space_ptr < data_ptr:
            space_block = disk[space_ptr]
            space_len = space_block.end - space_block.begin + 1
            if space_block.id == "." and space_len >= data_len:
                success = True
                break
            space_ptr += 1

        if success:
            # print("  Found match ", space_block)
            # Clear out data on right side
            data_block.id = "."
            disk[data_ptr] = data_block

            if not space_block or not space_len:
                raise ValueError
            if data_len == space_len:
                # Update empty space block to have id=whatever
                space_block.id = file_id
                disk[space_ptr] = space_block
            elif data_len < space_len:
                # Prepare new data block to insert
                new_data_block = Range(
                    file_id, space_block.begin, space_block.begin + data_len - 1
                )

                # Shorten existing space block
                space_block.begin = space_block.begin + data_len - 1 + 1
                disk[space_ptr] = space_block

                # Insert new data block
                disk.insert(space_ptr, new_data_block)

        # Go next
        file_id -= 1
    return disk


def consolidate(disk):
    # Find first empty space
    space_ptr = 0
    space_block = disk[space_ptr]
    while space_block.id != ".":
        if space_ptr + 1 >= len(disk):
            ## Couldn't find any space
            return disk, False
        space_ptr += 1
        space_block = disk[space_ptr]

    # Find last data value
    data_ptr = len(disk) - 1
    data_block = disk[data_ptr]
    while data_block.id == ".":
        if data_ptr - 1 < 0:
            ## Couldn't find any data
            return disk, False
        data_ptr -= 1
        data_block = disk[data_ptr]

    if space_block.begin > data_block.end:
        # print("Done!")
        return disk, False

    space_len = space_block.end - space_block.begin + 1
    data_len = data_block.end - data_block.begin + 1
    xfer_len = min(space_len, data_len)

    new_id = None

    # Shorten the data on the right
    if xfer_len == data_len:
        # Delete empty space block
        # TODO, Instead of deleting it we could do something else
        new_id = data_block.id
        del disk[data_ptr]
    elif xfer_len < data_len:
        new_id = data_block.id
        # Shorten data block
        data_block.end -= xfer_len
        disk[data_ptr] = data_block

        # Insert new empty space block
        new_space_block = Range(
            ".", data_block.end + 1, data_block.end + 1 + xfer_len - 1
        )
        disk.insert(data_ptr + 1, new_space_block)
    else:
        raise ValueError("Not expect to see xfer_len > data_len")

    # Insert the data on the left
    if xfer_len == space_len:
        # Update empty space block to have id=whatever
        space_block.id = new_id
        disk[space_ptr] = space_block
    elif xfer_len < space_len:
        # Prepare new data block to insert
        new_data_block = Range(
            new_id, space_block.begin, space_block.begin + xfer_len - 1
        )

        # Shorten existing space block
        space_block.begin = space_block.begin + xfer_len - 1 + 1
        disk[space_ptr] = space_block

        # Insert new data block
        disk.insert(space_ptr, new_data_block)
    else:
        raise ValueError("Not expect to see xfer_len > space_len")

    return disk, True


class Day09:
    """AoC 2024 Day 09"""

    @staticmethod
    def part1(filename: str) -> int:
        disk, _max_file_id = parse(filename)

        while True:
            disk, did_consolidate = consolidate(disk)
            if not did_consolidate:
                break
        return checksum(disk)

    @staticmethod
    def part2(filename: str) -> int:
        disk, max_file_id = parse(filename)

        disk = consolidate_whole_files_method(disk, max_file_id)
        return checksum(disk)
