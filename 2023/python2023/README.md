# Advent of Code 2023 in Python

## Requirements

- You must be in the `python2023` directory for paths to resolve correctly.
- You may need some extra python packages installed, like `numpy`. I have added a `requirements.txt` file.

## Setting Up the Python Virtual Environment

1. If you haven't already, install `virtualenv`:

```
pip install virtualenv
```

2. Create a virtual environment named `venv2023` in the python2023 directory:

```
virtualenv venv2023
```

3. Activate the virtual environment:

- For bash/zsh/sh:
  ```
  source venv2023/bin/activate
  ```
- For Fish shell:
  ```
  source venv2023/bin/activate.fish
  ```

4. Install the required packages:

```
pip install -r requirements.txt
```

## See Answers And Timings

`make`

## Verify Answers Are Correct

`make test`
