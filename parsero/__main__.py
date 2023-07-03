from tkinter.filedialog import askopenfilename

from termcolor import colored

import parsero
from parsero import *


def welcome_message():
    print(colored("Parsero " + parsero.__version__, "cyan") + "\n")
    print(
        """
        Integrantes do grupo:
        Anthony Bernardo Kamers (19204700)
        Gabriel da Silva Cardoso (20100524)
        Gabriel Holstein Meireles (19102918)
        Nicole Schmidt (18203344)
    """
    )


def parsero_cli():
    filename_regex = "examples/ConvCC-2023-1/regex.regex"
    filename_ghm = "examples/ConvCC-2023-1/gramatica.ghm"
    parsero_obj = Parsero(filename_regex, filename_ghm, True)
    while True:
        print("Forneça o arquivo para analisar")
        filename_word = askopenfilename(
            filetypes=[("ConvCC-2023-1 Files", ".lcc")], initialdir="examples/ConvCC-2023-1/"
        )
        print(parsero_obj.highlight(filename_word))
        print("Escolher outro arquivo?")
        if not boolean_select():
            break


def boolean_select() -> bool:
    selected = input("s/n: ")
    return selected.lower() == "s" or selected.lower() == "y"


# os.system("cls||clear")
welcome_message()
parsero_cli()
