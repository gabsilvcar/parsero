import os
import tkinter
from tkinter.filedialog import askopenfilenames

from termcolor import colored

import parsero
from parsero import *
from parsero.automata import *
from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import create_table, ll1_parse


def welcome_message():
    print(colored("Parsero " + parsero.__version__, "cyan") + "\n")


def select_analyser():
    print("Selecione o analisador a ser usado:")
    print("(0) Automatos Finitos")
    print("(1) Expressões Regulares")

    print("(2) Analisador Léxico")
    print("(3) Analisador Sintático")
    selected = number_input()
    match selected:
        case "0":
            start_automata()
        case "1":
            syntactic()
        case "2":
            lexical()
        case "3":
            syntactic()
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
        show_automata_list(built)
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
        pos = select_single_automata()
    else:
        pos = 0
    filename = input("Forneça o nome do arquivo. Ex: pasta/nome.fa: ")
    built[pos].to_file(filename)
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
    pos1 = select_single_automata()
    pos2 = select_single_automata()
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
    show_automata_list(built)
    selected = number_input()
    print(built[int(selected)])


def show_glc(built: list):
    show_glc_list(built)
    selected = number_input()
    print(built[int(selected)])


def show_automata_list(built: list):
    match len(built):
        case "0":
            file_not_valid()
        case "1":
            print("Automato finito carregado [0]")
        case _:
            print("Automatos finitos carregados [0, ..., {}]".format(len(built) - 1))


def show_glc_list(built: list):
    match len(built):
        case "0":
            file_not_valid()
        case "1":
            print("Gramática Livre de Contexto carregada [0]")
        case _:
            print("Gramáticas Livres de Contexto carregadas [0, ..., {}]".format(len(built) - 1))


def automata_file_select():
    filenames = select_files()
    if filenames:
        built = build_automata(filenames)
        return built
    else:
        return None


def regex():
    pass


def boolean_select() -> bool:
    selected = input("s/n: ")
    return selected.lower() == "s" or selected.lower() == "y"


def select_single_automata() -> int:
    print("Selecione o automato para fazer uma operação:")
    while True:
        selected = number_input()
        print(selected)
        print("Você deseja selecionar este automato?")
        if boolean_select():
            return int(selected)


def select_files():
    print("Selecione os arquivos a serem carregados.")
    tkinter.Tk().withdraw()
    filenames = askopenfilenames()

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
        pos = select_single_automata()
    else:
        pos = 0
    built[pos] = built[pos].determinize()
    print("Automato determinizado: ")
    print(built[pos])
    return built


def lexical():
    pass


def syntactic():
    files = select_files()
    cfg_list = load_cfgs(files)
    if cfg_list:
        syntactic_loop(cfg_list)
    else:
        pass


def select_glc(cfg_list) -> int:
    print("Selecione a GLC para fazer uma operação:")
    while True:
        selected = number_input()
        print(selected)
        print("Você deseja selecionar este automato?")
        if boolean_select():
            return int(selected)


def syntatic_parse(cfg_list):
    if len(cfg_list) > 1:
        pos = select_glc(cfg_list)
    else:
        pos = 0
    cfg = cfg_list[pos]
    print("Terminais: ", cfg.terminal_symbols)
    word_input = input("Forneça a palavra: ")
    word = word_input.split(" ")
    word.append("$")
    table: dict = create_table(cfg)
    print(ll1_parse(word, table, cfg))


def syntactic_loop(cfg_list):
    while True:
        show_glc_list(cfg_list)
        print("Selecione uma operação:")
        print("(0) Exibir GLC")
        print("(1) Preparar GLC")
        print("(2) Parsear LL(1)")
        print("(3) Voltar para o menu")

        selected = number_input()
        match selected:
            case "0":
                show_glc(cfg_list)
            case "1":
                pass  # TODO
            case "2":
                syntatic_parse(cfg_list)
            case "3":
                break
            case _:
                invalid_command()


def load_cfgs(filenames) -> list:
    cfg_list = []
    i = 0
    for file in filenames:
        built_cfg = ContextFreeGrammar(file)
        print(i, ": ", os.path.basename(file))
        print(built_cfg)
        i += 1
        cfg_list.append(built_cfg)
    return cfg_list


def invalid_command():
    print(colored("ERRO: entrada não reconhecida", "red"))


def file_not_valid():
    print(colored("ERRO: não foi selecionado um arquivo válido", "red"))


def wait_user():
    input("Pressione enter para o próximo passo")


def number_input() -> str:
    return input("Formato de entrada: 0, 1, 2, 3: ")


os.system("cls||clear")
welcome_message()
select_analyser()
