from itertools import permutations
from aoc.computer import Computer, solve1


def amplify_once_find_max_seq(program_in):
    """Try every combination of phase settings on the amplifiers. What is the
    highest signal that can be sent to the thrusters? (Max Val)"""
    max_val = 0
    max_sequence = []

    for seq in permutations([0, 1, 2, 3, 4]):
        phase_sequence = list(seq)
        val = amplify_once(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]


def amplify_once(program_in, phase_sequence):
    input_signal = 0
    for setting in phase_sequence:
        outputs = solve1(program_in, [setting, input_signal])
        input_signal = outputs[0]
    return input_signal


def amplify_loop(program_in, phase_sequence):
    cpus = []
    for i in range(5):
        cpus.append(Computer(program_in, [phase_sequence[i]]))

    i = 0
    next_input = 0
    while True:
        cpus[i].add_input(next_input)
        cpus[i].execute()
        if cpus[i].state == "halted" and i == 4:
            # print("halted")
            return cpus[i].outputs[0]
        next_input = cpus[i].pop_output()
        i = (i + 1) % 5


def amplify_loop_max_seq(program_in):
    max_val = 0
    max_sequence = []
    for seq in permutations([5, 6, 7, 8, 9]):
        phase_sequence = list(seq)
        val = amplify_loop(program_in, phase_sequence)
        if val > max_val:
            max_val = val
            max_sequence = phase_sequence
    return [max_val, max_sequence]
