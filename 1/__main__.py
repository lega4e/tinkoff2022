#!python3

import typer

from curses_adapter import CursesAdapter
from game import Game


def main(height: int, width: int):
    adapter = CursesAdapter()
    Game(adapter, height, width).run()
    exit(0)


if __name__ == "__main__":
    typer.run(main)
