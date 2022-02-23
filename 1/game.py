import curses
import pickle

from random import randint

from board   import Board
from cmdline import CmdLine
from color   import Color, init_colors
from command import Command, command_mode
from copy    import deepcopy
from hello   import Hello
from ship    import Ship, generate_ships
from status  import Status


def _mod(a: int, b: int) -> int:
  return (a + b) % b


def _stack2num(stack: [int]) -> int:
  val = 0
  for digit in stack:
    val = val * 10 + digit
  return val


def fill_rectangle(screen, y, x, h, w, *, sym = ' '):
  for yy in range(y, y+h):
    screen.addstr(yy, x, sym * w)


class Game:
    def __init__(self, height, width):
      ships = generate_ships(height, width)
      self.userboard = Board(height, width, deepcopy(ships))
      self.compboard = Board(height, width, ships)
      self.screen = self._make_screen()
      init_colors()
      self.h, self.w = self.screen.getmaxyx(); self.w -= 1
      self.hello = Hello(height, width)
      self.cmdln = CmdLine()

      if (
        not self._check_menu_required_size() or
        not self._check_game_required_size()
      ):
        curses.endwin()
        raise Exception("Screen too small, try to increase screen size")


    def execute_command(self, cmd: Command) -> bool:
      'Return True if need to quit program'
      if cmd.command == Command.QUIT:
        curses.endwin()
        return True
      elif cmd.command == Command.LOAD:
        try:
          (
            self.h, self.w,
            self.userboard, self.compboard,
            self.hello, self.cmdln
          ) = pickle.load(open(cmd.arg, 'rb'))
          self.screen.addstr(
            self.h-1, 0,
            self.cmdln.answer(1, self.w, 'Game loaded')
          )
        except Exception as e:
          self.screen.addstr(
            self.h-1, 0,
            self.cmdln.answer(
              1, self.w,
              "Can't find file '%s' or invalid format" % cmd.arg
            )
          )
      elif cmd.command == Command.SAVE:
        pickle.dump((
          self.h, self.w,
          self.userboard, self.compboard,
          self.hello, self.cmdln
        ), open(cmd.arg, 'bw'))
        self.screen.addstr(
          self.h-1, 0,
          self.cmdln.answer(1, self.w, 'Game saved')
        )
      return False


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
          if self.execute_command(command_mode(self.screen, self.cmdln)):
            break


    def run_game(self):
      usershots = []
      compshots = []
      digitstack = []
      crsy, crsx = 0, 1

      while True:
        self.draw_screen(usershots, compshots, crsy, crsx)
        self.screen.addstr(0, 0, str(digitstack))
        c = self.screen.getch()
        savestack = False
        if c == curses.KEY_LEFT:
          crsx = _mod(crsx - 1, self.compboard.w)
        elif c == curses.KEY_RIGHT:
          crsx = _mod(crsx + 1, self.compboard.w)
        elif c == curses.KEY_UP:
          crsy = _mod(crsy - 1, self.compboard.h)
        elif c == curses.KEY_DOWN:
          crsy = _mod(crsy + 1, self.compboard.h)
        elif ord('0') <= c <= ord('9'):
          savestack = True
          d = c - ord('0')
          digitstack.append(d)
          newy = _stack2num(digitstack) - 1
          if newy >= self.userboard.h:
            digitstack = [ d ]
            newy = d - 1
          if 0 <= newy < self.userboard.h:
            crsy = newy
        elif ord('a') <= c <= ord('z') or ord('A') <= c <= ord('Z'):
          newx = c - (ord('a') if ord('a') <= c <= ord('z') else ord('A'))
          if 0 <= newx < self.compboard.w:
            crsx = newx
        elif c == ord(' ') or c == ord('\n'):
          usershots.append((crsy, crsx))
        elif (
          c == ord(':') and
          self.execute_command(command_mode(self.screen, self.cmdln))
        ):
          break
        self.screen.addstr(0, 0, str(c))

        if not savestack:
          digitstack.clear()


    def draw_screen(self, usershots, compshots, crsy, crsx):
      bh, bw = self.userboard.required_size()
      vspace = (self.h - bh)
      vspaces = [ vspace - vspace // 2, vspace // 2 ]
      hspace = (self.w - bw * 2)
      hspaces = [ hspace // 3 ] * 3
      if hspace % 3 > 0: hspaces[0] += 1
      if hspace % 3 > 1: hspaces[1] += 1

      self.userboard.draw(
         self.screen,
         vspaces[0], hspaces[0],
         compshots, False
      )

      fill_rectangle(
         self.screen, vspaces[0], hspaces[0] + bw - 1,
         bh, hspaces[1] + 1
      )

      self.compboard.draw(
         self.screen,
         vspaces[0], sum(hspaces[:2]) + bw,
         usershots, True
      )

      crsy, crsx = self.userboard.board2screen(
        crsy, crsx,
        vspaces[0], sum(hspaces[:2]) + bw
      )

      self.screen.chgat(crsy, crsx, 1, curses.color_pair(Color.CURSOR))


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
