#!/usr/bin/env python
"""
Advent Of Code 2024 Day 24
https://adventofcode.com/2024/day/24
"""

def parse(filename):
    variables = {}
    operations = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            if ":" in line:  # This is a variable definition
                var, value = line.split(':')
                variables[var.strip()] = int(value.strip())
            elif "->" in line:  # This is an operation
                expression, result = line.split("->")
                expression = expression.strip()
                result = result.strip()

                # Handle XOR first since it contains 'OR'
                if "XOR" in expression:
                    op_type = "XOR"
                    left, right = expression.split("XOR")
                elif "AND" in expression:
                    op_type = "AND"
                    left, right = expression.split("AND")
                elif "OR" in expression:
                    op_type = "OR"
                    left, right = expression.split("OR")
                else:
                    raise ValueError(f"Unknown operation in: {expression}")

                operation = {
                    'type': op_type,
                    'left': left.strip(),
                    'right': right.strip(),
                    'output': result
                }
                operations.append(operation)

    return variables, operations

def evaluate_operation(op, variables):
    if op['left'] not in variables or op['right'] not in variables:
        return None

    if op['type'] == 'AND':
        result = variables[op['left']] & variables[op['right']]
    elif op['type'] == 'OR':
        result = variables[op['left']] | variables[op['right']]
    elif op['type'] == 'XOR':
        result = variables[op['left']] ^ variables[op['right']]
    else:
        raise ValueError()
    return result

def try_evaluate_all_operations(variables, operations):
    c = 0
    for op in operations:
        if op['output'] in variables:
            continue
        result = evaluate_operation(op, variables)
        if result is not None:  # Operation was ready to evaluate
            variables[op['output']] = result
            c += 1
    return c

def flip_ops(ops, out1, out2):
    # Make a deep copy so we don't modify original
    new_ops = ops.copy()
    # Find and swap the outputs
    for op in new_ops:
        if op['output'] == out1:
            op['output'] = out2
        elif op['output'] == out2:
            op['output'] = out1
    return new_ops

def find_full_adder_pattern(ops, start_bit):
    """Try to identify a full adder at bit position i by following connections"""
    patterns = {
        'sum_xor1': None,  # First XOR of x[i] and y[i]
        'carry_and1': None,  # First AND for x[i] and y[i]
        'sum_xor2': None,  # Second XOR with carry in
        'carry_and2': None,  # Second AND for carry
        'carry_or': None    # OR of the two carry sources
    }

    # Find initial XOR and AND of the input bits
    x_wire = f'x{str(start_bit).zfill(2)}'
    y_wire = f'y{str(start_bit).zfill(2)}'

    for op in ops:
        if (op['left'] == x_wire and op['right'] == y_wire) or \
           (op['left'] == y_wire and op['right'] == x_wire):
            if op['type'] == 'XOR':
                patterns['sum_xor1'] = op
            elif op['type'] == 'AND':
                patterns['carry_and1'] = op

    if not patterns['sum_xor1']:
        return patterns  # Can't find basic XOR, probably not a full adder

    # Follow the first XOR's output
    first_xor_out = patterns['sum_xor1']['output']
    for op in ops:
        # Look for ops that use the first XOR's output
        if op['left'] == first_xor_out or op['right'] == first_xor_out:
            if op['type'] == 'XOR':
                # This is probably the carry-in XOR
                patterns['sum_xor2'] = op
                # The other input to this XOR should be the carry in
                carry_in = op['right'] if op['left'] == first_xor_out else op['left']
                # Could store carry_in wire for debugging/verification
            elif op['type'] == 'AND':
                # This is probably the second carry AND
                patterns['carry_and2'] = op

    # If we found carry_and1, follow its output to find the OR
    if patterns['carry_and1']:
        first_carry = patterns['carry_and1']['output']
        for op in ops:
            if op['type'] == 'OR' and \
               (op['left'] == first_carry or op['right'] == first_carry):
                patterns['carry_or'] = op
                # The other input should connect to carry_and2's output
                if patterns['carry_and2']:
                    second_carry = patterns['carry_and2']['output']
                    if op['left'] == second_carry or op['right'] == second_carry:
                        # This confirms it's the carry OR gate
                        patterns['carry_or'] = op

    return patterns

def identify_clean_adders(ops):
    """Find full adders that look correct"""
    clean_ops = set()  # operations we're confident are correct
    suspect_ops = set()  # operations that should be part of an adder but look wrong

    # For each bit position...
    num_bits = 45
    for i in range(num_bits):
        pattern = find_full_adder_pattern(ops, i)
        print(i, pattern)
        # If we find a perfect match, add to clean
        # If we find almost matches, add to suspects

class Day24:
    """AoC 2024 Day 24"""

    @staticmethod
    def part1(filename: str) -> int:
        vars, ops = parse(filename)
        while True:
            c = try_evaluate_all_operations(vars, ops)
            print(c)
            if c == 0:
                break
        # for k in sorted(vars.keys()):
        #     print(k, vars[k])
        result = 0
        for k in reversed(sorted(vars.keys())):
            if k[0] != 'z':
                continue
            print(vars[k], end='')
            result = (result << 1) | vars[k]
        return result

    @staticmethod
    def part2(filename: str) -> int:
        vars, ops = parse(filename)
        new_ops = ops
        new_ops = flip_ops(new_ops, 'qqp', 'z23') # Like
        new_ops = flip_ops(new_ops, 'pbv', 'z16') # Like
        new_ops = flip_ops(new_ops, 'fbq', 'z36') # Like
        new_ops = flip_ops(new_ops, 'qnw', 'qff') # Like
        identify_clean_adders(new_ops)
