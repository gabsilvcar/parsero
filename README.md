# Parsero
Parsero is a lexical and syntactic analyzer made from scratch
(without the usage of any external libraries).

The only libraries used are for purposes of managing the project
and printing tables and other structures more beautifully.

In order to install and run this project, it is necessary:
* Python: at least version 3.10
  * https://www.python.org/downloads/release/python-31010/
* Poetry: version 1.4
  * https://python-poetry.org/docs/
  * It is necessary to have poetry in your $PATH
* Tkinter: necessary installation through Operating System (possible installation candidates below)
  * `sudo apt install python3-tk`
  * `sudo pacman -S tk` or `sudo pacman -S tk-dev` 

## Execution

The dependencies of this project are managed with poetry. Learn about it in https://python-poetry.org/.

**First, install the dependencies (it is necessary to have poetry installed):**

    make install

**Run it:**

    make

## Testing the lexical analyzer for INE5426
The grammar and regex from this semester are called: CC-2023-1.
In order to test the execution of Parsero, there are 3 example
files in `examples/CC-2023-1/`, starting with the name: `exemplo`.

### Testing
Step by Step to test the application:
* make
* 2
* select the regex file, located in `examples/CC-2023-1/regex.regex`
* n
* 1
* select some of the example files in `examples/CC-2023-1/exemplo*`
* n

That's it, the symbol table, as well as the tokens list will
be presented into the terminal.

To close the application properly from this point:
* 2
* 3

## Developer Tools

**Fix your code formating:**

    make format

**Execute tests:**

    make test

