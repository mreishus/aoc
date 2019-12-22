#!/usr/bin/env python

from collections import deque
import re


def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = (
            remainder,
            divmod(lastremainder, remainder),
        )
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return_x = lastx * (-1 if aa < 0 else 1)
    return_y = lasty * (-1 if bb < 0 else 1)
    return lastremainder, return_x, return_y


def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def parse_22(filename):
    """ Parse the input file into a list of commands.
    Commands are tuples.  There are 3 possible commands:
    ("cut", 5)
    ("dealsnc", 9)
    ("dealnew", None)
    """
    data = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            # print(line)
            cut_match = re.match("^cut (-?\d+)", line)
            deal_inc_match = re.match("^deal with increment (\d+)", line)
            deal_new_match = re.match("^deal into new stack", line)
            if cut_match:
                [amount] = cut_match.groups()
                data.append(("cut", int(amount)))
            if deal_inc_match:
                [amount] = deal_inc_match.groups()
                data.append(("dealinc", int(amount)))
            if deal_new_match:
                data.append(("dealnew", None))
    return data


def simulate(data, deck_size, deck=None):
    """ Given a list of shuffle commands (data), and a deck size,
    simulate shuffling a deck using a deque. Returns the deck (deque). """
    if deck is None:
        deck = deque(range(deck_size))
    for (command, arg) in data:
        if command == "dealnew":
            deck = deque(reversed(deck))
        if command == "cut":
            deck.rotate(arg * -1)
        if command == "dealinc":
            new_deck = [None] * len(deck)
            i = 0
            decklen = len(deck)
            for j in range(decklen):
                item = deck.popleft()
                new_deck[i] = item
                i = (i + arg) % decklen
            deck = deque(new_deck)
            new_deck = None
    return deck


def shuffle_to_mb(data, deck_size):
    """ Given a list of shuffle commands (data), and a deck size,
    return "m" and "b" parameters of a linear equation describing
    the shuffled deck.  That is, each shuffle is a linear transformation
    like so:

    card = m * i + b.

    It is always safe to set m = m % deck_size, or b = b % deck_size.

    An unshuffled deck, for example, is m = 1, b = 0, such that
    card = i.  Deck[5] = 5.

    Cutting 3 cards moves b forward by m * 3.  Cutting an unshuffled
    deck by 3 is m = 1, b = 3. Deck[5] = 8.

    Reversing the deck ("dealnew") sets m = m * 1, and increments b by m.

    Dealinc.. is complicated.  If we're dealincing a 10 card deck by 3,
    we want to solve the equation 3 * ? % 10 = 1.  So we use modinv,
    which I had to google for.

    0 1 2 3 4 5 6 7 8 9  Deck before Dealinc
    0 7 4 1 8 5 2 9 6 3  Deck after Dealinc 3.
      ^
      \- Solve 3 * ? % 10 = 1.  Answer is 7: 3 * 7 = 21. 21 % 10 = 1
    """

    # y = mx + b
    m = 1
    b = 0
    for (command, arg) in data:
        if command == "dealnew":
            m *= -1
            b = (b + m) % deck_size
        if command == "cut":
            b = (b + (arg * m)) % deck_size
        if command == "dealinc":
            m = (m * modinv(arg, deck_size)) % deck_size
    return m, b


def mb_to_gen(m, b, deck_size):
    """ Given the parameters of a linear equation, m and b, as well as a deck size,
    return a generator that returns the entire deck when iterated over. """
    for i in range(deck_size):
        yield (m * i + b) % deck_size


def part1_simulate(data, deck_size, search_for_value):
    """ After shuffling your factory order deck of deck_size cards,
    what is the position of card search_for_value?
    Uses simulation method to solve. """
    results = simulate(data, deck_size)
    for i, val in enumerate(results):
        if val == search_for_value:
            return i
    return None


def part1_linear(data, deck_size, search_for_value):
    """ After shuffling your factory order deck of deck_size cards,
    what is the position of card search_for_value?
    Uses linear equation method to solve. """
    m, b = shuffle_to_mb(data, deck_size)
    results = mb_to_gen(m, b, deck_size)
    for i, val in enumerate(results):
        if val == search_for_value:
            return i
    return None


def multiple_shuffle_simulate(data, deck_size, times):
    deck = deque(range(deck_size))
    for i in range(times):
        deck = simulate(data, deck_size, deck=deck)
    return deck


def double_mb(m, b, deck_size):
    """
    y = mx + b

    Can be done by matrix multiplication:

    [ y    = [ m  b   [ x
      1 ]      0  1 ]   1 ]

    If we want m and b for applying the linear transformation twice,
    we can square the matrix in the middle

    [ m b   [ m b     = [ m*m  m*b + b*1
      0 1 ]   0 1 ]        0        1    ]

    new_m (m for running mx+b twice) = m * m
    new_b (b for running mx+b twice) = m*b + b

    This takes in an m, b for shuffling a deck a certain amount
    of times, and returns the m, b for shuffling that deck
    double the number of times.
    """
    new_m = (m * m) % deck_size
    new_b = (m * b + b) % deck_size
    return new_m, new_b


def add_mb(m1, b1, m2, b2, deck_size):
    """
    Instead of multiplying a matrix by itself,
    multiply two m b matricies.

    This way, if we have m,b for applying the shuffle 16 times,
    and m,b for applying shuffle 4 times, we can multiply those two
    together to get m,b for applying shuffle 20 times.


    [m1 b1  [m2 b2   = [ m1 * m2  m1 * b2 + b1
     0  1]    0 1 ]        0          1        ]
    """
    new_m = (m1 * m2) % deck_size
    new_b = (m1 * b2 + b1) % deck_size
    return new_m, new_b


def multiple_shuffle_to_mb(data, deck_size, times):
    mb_for_step = {}

    m1, b1 = shuffle_to_mb(data, deck_size)
    m, b = m1, b1
    i = 1
    mb_for_step[1] = (m1, b1)

    while i < times:
        # We currently have m, b for shuffling the deck "i" times.
        # But we want to shuffle the deck "times" times.
        if i * 2 < times:
            # If we can double the number of times we shuffle, go for it.
            m, b = double_mb(m, b, deck_size)
            i *= 2
            mb_for_step[i] = (m, b)
        else:
            # Otherwise, add the highest number of shuffles we've seen that still
            # fits.  For example, if we have 16 shuffles, and we're aiming for 20,
            # we can do add_mb(16 shuffles, 4 shuffles) to get 20 shuffles.
            next_step = max(v for v in mb_for_step.keys() if v <= times - i)
            (step_m, step_b) = mb_for_step[next_step]
            m, b = add_mb(m, b, step_m, step_b, deck_size)
            i += next_step
            mb_for_step[i] = (m, b)
    return m, b


def multiple_shuffle_linear(data, deck_size, times):
    m, b = multiple_shuffle_to_mb(data, deck_size, times)
    return list(mb_to_gen(m, b, deck_size))


def part2(data, deck_size, times, index):
    m, b = multiple_shuffle_to_mb(data, deck_size, times)
    return (m * index + b) % deck_size


if __name__ == "__main__":
    ## Part 1
    # After shuffling your factory order deck of 10007 cards, what is the position of card 2019
    data = parse_22("../../22/input.txt")
    p1_answer = part1_simulate(data, 10007, 2019)
    p1_answer2 = part1_linear(data, 10007, 2019)
    print(f"Part 1: {p1_answer} or {p1_answer2}")

    ## Part 2
    data = parse_22("../../22/input.txt")
    part2_decksize = 119315717514047
    part2_times = 101741582076661
    p2_answer = part2(data, part2_decksize, part2_times, 2020)
    print(f"Part 2: {p2_answer}")
