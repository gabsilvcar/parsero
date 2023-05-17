from parsero import Parsero


def test_ine5426():
    parser = Parsero(
        f"examples/ConvCC-2023-1/regex.regex", f"examples/ConvCC-2023-1/gramatica.ghm", True
    )
    parser.parse(f"examples/ConvCC-2023-1/exemplo1.lcc")  # TODO
