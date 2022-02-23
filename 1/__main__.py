#!python3

import typer

from game import Game


def main(height: int, width: int):
    Game(height, width).run()
    exit(0)


if __name__ == "__main__":
    typer.run(main)
