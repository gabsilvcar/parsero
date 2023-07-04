from parsero import Parsero


def test_ine5426():
    parser = Parsero(
        # f"examples/ConvCC-2023-1/regex.regex", f"examples/ConvCC-2023-1/GCI/convcc-2023-1.ghm12", True
        f"examples/ConvCC-2023-1/regex.regex", f"examples/ConvCC-2023-1/gramatica.ghm", True

    )
    parser.cfg.to_file("convcc-2023-1.ghm12")
    parser.parse(f"examples/ConvCC-2023-1/exemplo1.lcc")  # TODO
