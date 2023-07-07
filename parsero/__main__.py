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

def run_cli():
        print(
"""
Escolha a gramatica desejada para o Parsero  
(1) Gramatica EXPA (DEC + Expressões aritméticas - completo)
            (arq. de exemplo: exemplo 1-3.lcc, gramatica_expa.lcc)
(2) Gramatica DEC (Apenas declarações)
            (arq. de exemplo: exemplo_dec.lcc)
(3) Gramatica Geradora de Código Intermediário
            (arq. de exemplo: exemplo_gci.lcc)
(0) Sair
""")
    
        param = []
        choice = str(input())
        while choice not in ["0", "1", "2", "3"]:
            print("Escolha invalida. Escolha entre 0-3")
            run_cli()
            return

        if choice == "0":
            return
        elif choice == "1":
            param = expa_param
        elif choice == "2":
            param = dec_param
        elif choice == "3":
            param = gci_param
    
        parsero_cli(param)

def parsero_cli(fileparam):
    filename_regex = fileparam[0]
    filename_ghm = fileparam[1]
    filename_semantic_lib = fileparam[2]
    parsero_obj = Parsero(filename_regex, filename_ghm, False, filename_semantic_lib)
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

expa_param = ["examples/ConvCC-2023-1/regex.regex", 
              "examples/ConvCC-2023-1/EXPA/gramatica_EXPA.ghm12", 
              "examples/ConvCC-2023-1/EXPA/semantics/__init__.py"]

dec_param = ["examples/ConvCC-2023-1/regex.regex",
             "examples/ConvCC-2023-1/DEC/gramatica_DEC.ghm12",
             "examples/ConvCC-2023-1/DEC/semantics/__init__.py"]

gci_param = ["examples/ConvCC-2023-1/regex.regex",
             "examples/ConvCC-2023-1/GCI/gramatica_GCI.ghm12",
             "examples/ConvCC-2023-1/GCI/semantics/__init__.py"]
# os.system("cls||clear")
welcome_message()
run_cli()
