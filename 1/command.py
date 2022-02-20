import curses

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
    return f'<Command {self.command} {self.arg}>'


def command_mode(screen, cmdline: CmdLine):
  h, w = screen.getmaxyx()
  w -= 1

  screen.addstr(h-1, 0, cmdline.tostr_hint(1, w))
  curses.echo()
  curses.curs_set(1)
  screen.move(h-1, 1)

  inp = screen.getstr().decode()
  p = inp.find(' ')
  if p >= 0:
    com = Command(inp[:p], inp[p+1:])
  else:
    com = Command(inp, None)

  com.command = { 
    'save' : Command.SAVE,
    'load' : Command.LOAD,
    'quit' : Command.QUIT,
  }.get(com.command, Command.ERROR)

  if com.command == Command.ERROR:
    screen.addstr(h-1, 0, lefted_str(' Error', w))

  curses.noecho()
  curses.curs_set(0)
  screen.getch()

  return com
