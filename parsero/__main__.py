import os
import tkinter
from tkinter.filedialog import askopenfilenames

from termcolor import colored

import parsero
from parsero import *
from parsero.automata import *
from parsero.common import LexicalError
from parsero.lexical import LexicalAnalyzer


def welcome_message():
    print(colored("Parsero " + parsero.__version__, "cyan") + "\n")


def select_analyser():
    while True:
        print("Selecione o analisador a ser usado:")
        print("(0) Automatos Finitos")
        print("(1) Expressões Regulares")
        print("(2) Analisador Léxico")
        print("(3) Encerrar Execução")
        selected = number_input()
        match selected:
            case "0":
                start_automata()
            case "1":
                while True:
                    regex_exp = input("Forneça a expressão regular: ")
                    while True:
                        word = input("Forneça a palavra: ")
                        automata = regex.compiles(regex_exp)
                        print(automata.evaluate(word))
                        print("Continuar com a mesma expressão regular?")
                        if not boolean_select():
                            break
                    print("Escrever outra expressão regular?")
                    if not boolean_select():
                        break
            case "2":
                lexical_cli()
            case "3":
                break
            case _:
                invalid_command()


def lexical_cli():
    print("Forneça as expressões regulares")
    files = select_files([("Expressões Regulares", ".regex")])
    lexical_list = load_lexical(files)
    if lexical_list:
        lexical_loop(lexical_list)
    else:
        pass


def lexical_loop(lexical_list):
    while True:
        print("Selecione uma operação:")
        print("(0) Exibir automato gerado")
        print("(1) Parsear")
        print("(2) Voltar para o menu")

        selected = number_input()
        match selected:
            case "0":
                selected = select_single_regex(lexical_list)
                print(lexical_list[selected].machine)
            case "1":
                selected = select_single_regex(lexical_list)
                print("Forneça o arquivo a ser analisado")
                files = select_files([("All Files", "*")])
                for file in files:
                    try:
                        result = lexical_list[selected].parse(file)
                        print("Lista de Tokens: ")
                        print(result[0])
                        print("Tabela de Símbolos: ")
                        print(result[1])
                        print("Sucesso!")
                    except LexicalError as e:
                        print("Essa palavra não pode ser gerada a partir das definições regulares. Erro: " + str(e))
            case "2":
                break
            case _:
                invalid_command()


def start_automata():
    built = automata_file_select()
    if built:
        automata_loop(built)
    else:
        pass


def automata_loop(built):
    while True:
        print("Selecione uma operação:")
        print("(0) Exibir automato")
        print("(1) Unir automatos")
        print("(2) Determinizar automato")
        print("(3) Salvar automato")
        print("(4) Voltar para o menu")

        selected = number_input()
        match selected:
            case "0":
                show_automata(built)
            case "1":
                built = unite(built)
            case "2":
                built = determinize_automata(built)
            case "3":
                save_automata(built)
            case "4":
                break
            case _:
                invalid_command()


def save_automata(built: list):
    if len(built) > 1:
        pos = select_single_automata(built)
    else:
        pos = 0
    filename = input("Forneça o nome do arquivo. Ex: pasta/nome.fa: ")
    automata_to_file(built[pos], filename)
    print("Arquivo salvo com sucesso!")


def unite(built: list):
    print("Selecione uma operação:")
    print("(0) Unir dois")
    print("(1) Unir todos")
    match number_input():
        case "0":
            return unite_two(built)
        case "1":
            return unite_all(built)
        case _:
            invalid_command()
            return built


def unite_two(built: list):
    pos1 = select_single_automata(built)
    pos2 = select_single_automata(built)
    if pos1 > pos2:  # avoids index change between operations
        automata1 = built[pos1].pop()
        automata2 = built[pos2].pop()
    else:
        automata2 = built[pos2].pop()
        automata1 = built[pos1].pop()

    nd_fa = NDFiniteAutomata.union(automata1, automata2)

    built.append(nd_fa)

    print("Automato determinizado: ")
    print(built)
    return built


def unite_all(built: list):
    built = [automata.union(*built)]
    print("Resultado da união dos automatos (ND):")
    print(built[0])
    return built


def show_automata(built: list):
    selected = select_single_automata(built)
    print(built[int(selected)])


def show_automata_list(built: list):
    match len(built):
        case 0:
            file_not_valid()
        case 1:
            print("Automato finito carregado [0]")
        case _:
            print("Automatos finitos carregados [0, ..., {}]".format(len(built) - 1))


def show_regex_list(built: list):
    match len(built):
        case 0:
            file_not_valid()
        case 1:
            print("Expressão regular carregada [0]")
        case _:
            print("Expressões regulares carregadas [0, ..., {}]".format(len(built) - 1))


def automata_file_select():
    filenames = select_files([("Automatos Finitos", ".ndfa .fa")])
    if filenames:
        built = build_automata(filenames)
        return built
    else:
        return None


def boolean_select() -> bool:
    selected = input("s/n: ")
    return selected.lower() == "s" or selected.lower() == "y"


def select_single_automata(built) -> int:
    if len(built) == 1:
        return 0

    print("Selecione o automato para fazer uma operação:")
    while True:
        selected = number_input()
        print(selected)
        print("Você deseja selecionar este automato?")
        if boolean_select():
            return int(selected)


def select_single_regex(built) -> int:
    if len(built) == 1:
        return 0

    print("Selecione o regex para fazer a análise:")
    while True:
        selected = number_input()
        print(selected)
        print("Você deseja selecionar este regex?")
        if boolean_select():
            return int(selected)


def select_files(file_types: list):
    print("Selecione os arquivos a serem carregados.")
    tkinter.Tk().withdraw()
    filenames = askopenfilenames(filetypes=file_types, initialdir="examples")

    while True:
        print("Você quer selecionar mais arquivos?")
        if boolean_select():
            tkinter.Tk().withdraw()
            filenames += askopenfilenames()
        else:
            break

    if filenames:
        return filenames
    else:
        return None


def build_automata(filenames):
    automata_list = []
    i = 0
    for file in filenames:
        built_automata = file_to_automata(file)
        print(i, ": ", os.path.basename(file))
        print(built_automata)
        i += 1
        automata_list.append(built_automata)
    return automata_list


def determinize_automata(built: list) -> list:
    if len(built) > 1:
        pos = select_single_automata(built)
    else:
        pos = 0
    built[pos] = built[pos].determinize()
    print("Automato determinizado: ")
    print(built[pos])
    return built


def load_lexical(filenames) -> list:
    lexical_list = []
    i = 0
    for file in filenames:
        built_lexical = LexicalAnalyzer(file)
        print(i, ": ", os.path.basename(file))
        print(built_lexical)
        i += 1
        lexical_list.append(built_lexical)
    return lexical_list


def invalid_command():
    print(colored("ERRO: entrada não reconhecida", "red"))


def file_not_valid():
    print(colored("ERRO: não foi selecionado um arquivo válido", "red"))


def wait_user():
    input("Pressione enter para o próximo passo")


def number_input() -> str:
    return input("Formato de entrada: 0, 1, ... n: ")


# os.system("cls||clear")
welcome_message()
select_analyser()
