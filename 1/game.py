import curses

from board   import Board, generate_ships
from command import command_mode
from cmdline import CmdLine
from hello   import Hello


class Game:
  def __init__(self, height, width):
    self.screen = self._make_screen()
    self.h, self.w = self.screen.getmaxyx(); self.w -= 1
    self.userboard = Board(height, width)
    self.compboard = Board(height, width)
    self.hello = Hello(height, width)
    self.cmdln = CmdLine()

    if (
      not self._check_menu_required_size() or
      not self._check_game_required_size()
    ):
      raise Exception("Screen too small, try to increase screen size")


  def run(self):
    self.screen.addstr(0, 0, self.hello.tostr(self.h-1, self.w))
    self.screen.addstr(self.h-1, 0, self.cmdln.tostr_prompt(1, self.w))
    self.screen.keypad(True)

    while True:
      key = self.screen.getkey()
      if key == '\n':
        exit(1)
      elif key == ':':
        command = command_mode(self.screen, self.cmdln)
        print(command)


  def _make_screen(self):
    screen = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(True)
    curses.start_color()
    return screen


  def _check_menu_required_size(self):
    hh, hw = self.hello.required_size()
    ch, cw = self.cmdln.required_size()
    return hh + ch <= self.h and max(hw, cw) <= self.w


  def _check_game_required_size(self):
    bh, bw = self.userboard.required_size()
    ch, cw = self.cmdln.required_size()
    return bh + ch <= self.h and max(cw, bw*2 + 1) <= self.w


