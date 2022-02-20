import curses
import pickle

from board   import Board, generate_ships
from command import Command, command_mode
from cmdline import CmdLine
from hello   import Hello


class Game:
  def __init__(self, height, width):
    ships = generate_ships(height, width)
    self.userboard = Board(height, width, ships)
    self.compboard = Board(height, width, ships)
    self.screen = self._make_screen()
    self.h, self.w = self.screen.getmaxyx(); self.w -= 1
    self.hello = Hello(height, width)
    self.cmdln = CmdLine()

    if (
      not self._check_menu_required_size() or
      not self._check_game_required_size()
    ):
      curses.endwin()
      raise Exception("Screen too small, try to increase screen size")


  def run(self):
    self.screen.addstr(0, 0, self.hello.tostr(self.h-1, self.w))
    self.screen.addstr(self.h-1, 0, self.cmdln.tostr_prompt(1, self.w))
    self.screen.keypad(True)

    while True:
      key = self.screen.getkey()
      if key == '\n':
        self.run_game()
        curses.endwin()
        break
      elif key == ':':
        com = command_mode(self.screen, self.cmdln)
        if com.command == Command.QUIT:
          curses.endwin()
          break
        elif com.command == Command.LOAD:
          try:
            (
              self.h, self.w,
              self.userboard, self.compboard,
              self.hello, self.cmdln
            ) = pickle.load(open(com.arg, 'rb'))
            self.screen.addstr(
              self.h-1, 0,
              self.cmdln.answer(1, self.w, 'Game loaded')
            )
          except Exception as e:
            self.screen.addstr(
              self.h-1, 0,
              self.cmdln.answer(
                1, self.w,
                "Can't find file '%s' or invalid format" % com.arg
              )
            )
        elif com.command == Command.SAVE:
          pickle.dump((
            self.h, self.w,
            self.userboard, self.compboard,
            self.hello, self.cmdln
          ), open(com.arg, 'bw'))
          self.screen.addstr(
            self.h-1, 0,
            self.cmdln.answer(1, self.w, 'Game saved')
          )

    print('END GAME', flush=True)


  def run_game(self):
    self.draw_screen()
    self.screen.getch()
    pass


  def draw_screen(self):
    bh, bw = self.userboard.required_size()
    vspace = (self.h - bh)
    vspaces = [ vspace - vspace // 2, vspace // 2 ]
    hspace = (self.w - bw * 2)
    hspaces = [ hspace // 3 ] * 3
    if hspace % 3 > 0: hspaces[0] += 1
    if hspace % 3 > 1: hspaces[1] += 1

    userboard = self.userboard.tostr().split('\n')
    compboard = self.compboard.tostr().split('\n')
    boards = '\n'.join([
      ' ' * hspaces[0] + userboard[i] + ' ' * hspaces[1] + compboard[i]
      for i in range(len(userboard))
    ])
    self.screen.addstr(vspaces[0], 0, boards)


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
    return bh + ch <= self.h and max(cw, bw*2 + 3) <= self.w


