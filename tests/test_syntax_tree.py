import importlib.util

from parsero import Parsero


def test():
    base = "examples/simple_syntax_tree/"
    path = base + "sst"
    parser = Parsero(
        path + ".regex",
        path + ".ghm12",
        base + "/semantics/__init__.py",
        False,
    )
    parser.parse(path + ".example")