# Parsero
Parsero is a lexical and syntactic analyzer made from scratch
(without the usage of any external libraries).

The only libraries used are for purposes of managing the project
and printing tables and other structures more beautifully.

The project have the following members:
* Anthony Bernardo Kamers (19204700)
* Gabriel da Silva Cardoso (20100524)
* Gabriel Holstein Meireles (19102918)
* Nicole Schmidt (18203344)

In order to install and run this project, it is necessary:
* Python: at least version 3.10
  * https://www.python.org/downloads/release/python-31010/
* Poetry: version 1.4
  * https://python-poetry.org/docs/
  * It is necessary to have poetry in your $PATH
* Tkinter: necessary installation through Operating System (possible installation candidates below)
  * `sudo apt install python3-tk`
  * `sudo pacman -S tk` or `sudo pacman -S tk-dev` 

The project is started using the default regex and grammar files, located in
`examples/ConvCC-2023-1`, requested by the teacher. You can normally change the
locations in the code, in `parsero/__main__.py` in lines 14 and 15 or change
directly the files in the examples folder.

## Execution

The dependencies of this project are managed with poetry. Learn about it in https://python-poetry.org/.

**First, install the dependencies (it is necessary to have poetry installed):**

    make install

**Run it:**

    make

## Developer Tools

**Fix your code formating:**

    make format

