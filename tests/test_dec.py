from parsero import Parsero


def test():
    base = "examples/ConvCC-2023-1/"
    dec = base + "DEC/"
    parser = Parsero(
        base + "regex.regex",
        dec + "gramatica_DEC.ghm12",
        False,
        dec + "semantics/__init__.py",
    )

    tree = parser.parse(dec + "/DEC.example")
    parser.semantic_analysis(tree)
    # assert (tree.find("VARDECL") == "string")

    print(tree)