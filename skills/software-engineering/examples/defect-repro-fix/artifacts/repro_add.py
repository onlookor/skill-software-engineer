import sys

sys.path.insert(0, ".")
from calc import add


def observe():
    return {"sum": add(2, 3)}
