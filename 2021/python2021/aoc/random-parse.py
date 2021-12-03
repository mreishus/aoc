def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))


def positive_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"\d+", s))


def floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+", s)


PARSER = re.compile(r"thing (\d+),(\d+), stuff")
