# Python

## Prereqs

```fish
# Install anaconda (Download and run .sh file from their website
### after anaconda is installed
conda create --name myenv --clone base
conda activate myenv
conda install black
conda install -c conda-forge neovim
## Networkx / sympy / numpy will already be installed
```

## Basic Setup

```fish
conda activate myenv
set PROJNAME python_day01
set FILENAME day01
mkdir $PROJNAME
cd $PROJNAME
nvim {$FILENAME}.py test_{$FILENAME}.py Makefile -p
```

## Note

See [2019/04](../2019/04/python_day04/) for an example of testing
without classes.

## `day01.py`

```python
#!/usr/bin/env python3
"""
Advent of Code 2017 Day 01.
"""


class Day01:
    """Main module for solving Day01."""

    def __init__(self, name):
        self.name = name
        self.zero = 0

    def add_one_class(self, input_val: int) -> int:
        """Add one to a number, and example of class function."""
        return input_val + 1 + self.zero

    @staticmethod
    def add_two_static(input_val):
        """Blah blah
        Example of static method."""
        return input_val + 2


if __name__ == "__main__":
    print("Hello from main")
```

## `test_day01.py`

```python
#!/usr/bin/env python3
"""
Test Day01.
"""

import unittest
from day01 import Day01


class TestBasic(unittest.TestCase):
    """Test Day01."""

    def test_static(self):
        """Test add_two_static"""
        got = Day01.add_two_static(5)
        want = 7
        self.assertEqual(got, want)

    def test_class(self):
        """Test add_one_class"""
        day_1 = Day01("Unused name")
        got = day_1.add_one_class(5)
        want = 6
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
```

## `./Makefile` (requires tabs!)

```make
run:
        python ./day01.py
test:
        pytest
repl:
        ipython
format:
        black .
```
