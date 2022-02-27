import curses

from curses_adapter import CursesAdapter
from cmdline import CmdLine
from utils import lefted_str


class Command:
    ERROR = -1
    SAVE = 0
    LOAD = 1
    QUIT = 2

    def __init__(self, command, arg):
        self.command = command
        self.arg = arg

    def __repr__(self):
        return f"<Command {self.command} {self.arg}>"


def fetch_command(adapter: CursesAdapter, cmdline: CmdLine) -> Command:
    screen = adapter.get_screen()
    h, w = screen.getmaxyx()
    w -= 1

    screen.addstr(h - 1, 0, cmdline.tostr_hint(1, w))
    screen.move(h - 1, 1)
    adapter.command_mode()

    inp = screen.getstr().decode().strip()
    p = inp.find(" ")
    if p >= 0:
        com = Command(inp[:p], inp[p + 1 :])
    else:
        com = Command(inp, None)

    com.command = {
        "save": Command.SAVE,
        "load": Command.LOAD,
        "quit": Command.QUIT,
    }.get(com.command, Command.ERROR)

    if com.command == Command.ERROR or (
        (com.command == Command.LOAD or com.command == Command.SAVE) and com.arg is None
    ):
        error = (
            " Error: unknown command"
            if com.command == Command.ERROR else
            " Error: should be file name"
        )
        com.command = Command.ERROR
        screen.addstr(h - 1, 0, lefted_str(error, w))

    adapter.game_mode()
    return com
