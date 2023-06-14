import importlib.util

from parsero import Parsero


def test():
    path = "examples/simple_syntax_tree/sst"
    parser = Parsero(
        path + ".regex",
        path + ".ghm12",
        path + ".py",
        False,
    )
    parser.parse(path + ".example")
