from parsero import Parsero


def test():
    base = "examples/ConvCC-2023-1/"
    parser = Parsero(
        base + "/regex.regex",
        base + "/gramatica_DEC.ghm",
        False,
        "examples/simple_syntax_tree/semantics/__init__.py",
    )

    tree = parser.parse(base + "/teste.example")
    print(tree)
