#!python3

import typer

from curses_adapter import CursesAdapter
from game import Game
from sys import stderr


def main(height: int, width: int):
    try:
        adapter = CursesAdapter()
        Game(adapter, height, width).run()
        exit(0)
    except Exception as e:
        print(e, file=stderr)
        exit(1)


if __name__ == "__main__":
    typer.run(main)
