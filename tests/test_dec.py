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

    tree, st = parser.parse(dec + "/DEC.example")
    print(tree)
    parser.semantic_analysis(tree, st)
    # assert (tree.find("VARDECL") == "string")


test()
