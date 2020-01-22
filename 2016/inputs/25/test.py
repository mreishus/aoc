#!/usr/bin/env python

with open('input.txt') as fp:
    lines = fp.read().strip().splitlines()

transforms = {
    'cpy': 'i +=1; {1} = {0}',
    'inc': 'i +=1; {0} += 1',
    'dec': 'i +=1; {0} -= 1',
    'jnz': 'i += {1} if {0}!=0 else 1; continue',
    'out': 'i += 1; yield({0})'
}


for a in range(1000):
    N = len(lines)
    program = ['def solve():']
    program += ['\ti=a=b=c=d=0']
    program += ['\ta=%s' % a]
    program += ['\twhile 0 <= i < {N}:'.format_map(locals())]
    for i, line in enumerate(lines):
        ins, *args = line.split(' ')
        code = transforms[ins].format(*args)
        program += ['\t\tif i=={i}: {code};'.format(i=i, code=code)]
    program = '\n'.join(program)
    exec(program)
    g = solve()
    x = 10
    s = ''.join(str(next(g)) for _ in range(x*2))
    if s.startswith('01'*x):
        print(s)
        print(a)
        exit()
