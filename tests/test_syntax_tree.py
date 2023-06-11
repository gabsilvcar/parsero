from parsero import Parsero


def test():
    parser = Parsero(
        f"examples/simple_syntax_tree/sst.regex", f"examples/simple_syntax_tree/sst.ghm12"
    )
    parser.parse(f"examples/simple_syntax_tree/sst.example")
