import copy
import curses

from color  import Color
from random import randint
from ship   import Ship



class Board:
  HORIZONTAL_SIGNS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  MAX_W            = len(HORIZONTAL_SIGNS)
  EMPTY            = ' '
  SHIP             = '■'
  HURT             = 'X'
  MISS             = '·'
  HORIZONTAL       = '─'
  VERTICAL         = '│'
  TOPLEFT          = '┌'
  TOPRIGHT         = '┐'
  DOWNLEFT         = '└'
  DOWNRIGHT        = '┘'


  def __init__(self, h: int, w: int, ships: [ Ship ] = None):
    self.w = w
    self.h = h
    if ships is not None:
      self.arrange_ships(ships)
    else:
      self.clear()


  def clear(self):
    self._d = [ [Board.EMPTY] * self.w for i in range(self.h) ]


  def arrange_ships(self, ships: [ Ship ]):
    self.ships = sorted(ships, key=lambda s: s.l, reverse=True)

    self.clear()
    for i in range(1000):
      if all([ self._arrange_ship(ship) for ship in self.ships ]):
        return True
    raise Exception("Error: can't arrange ships; try to increase board size")


  def _check_ship(self, ship: Ship) -> bool:
    my = ship.y if ship.hor else ship.y + ship.l - 1
    mx = ship.x if not ship.hor else ship.x + ship.l - 1
    if ship.x < 0 or mx >= self.w or ship.y < 0 or my >= self.h:
      return False

    for y in range(ship.y-1, my+2):
      if y >= self.h:
        break
      for x in range(ship.x-1, mx+2):
        if x >= self.w:
          break
        if self._d[y][x] != Board.EMPTY:
          return False

    return True


  def _place_ship(self, ship: Ship):
    if ship.hor:
      for x in range(ship.x, ship.x+ship.l):
        self._d[ship.y][x] = Board.SHIP
    else:
      for y in range(ship.y, ship.y+ship.l):
        self._d[y][ship.x] = Board.SHIP


  def _arrange_ship(self, ship: Ship) -> bool:
    for i in range(self.w * self.h):
      ship.y, ship.x = randint(0, self.h-1), randint(0, self.w-1)
      ship.hor = randint(0, 1)
      if self._check_ship(ship):
        self._place_ship(ship)
        return True
    return False


  def _is_kill(self, board, y, x):
    if board[y][x] != Board.HURT:
      return False
    ways = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for way in ways:
      yy, xx = y, x
      while yy >= 0 and yy < self.h and xx >= 0 and xx < self.w:
        if (
          board[yy][xx] == Board.SHIP or
          (board[yy][xx] == Board.EMPTY and self._d[yy][xx] == Board.SHIP)
        ):
          return False
        if board[yy][xx] != Board.HURT:
          break
        yy += way[0]
        xx += way[1]
    return True


  def _translate_board(self, shots, hide):
    board = copy.deepcopy(self._d)
    for y, x in shots:
      if board[y][x] == Board.EMPTY:
        board[y][x] = Board.MISS
      elif board[y][x] == Board.SHIP:
        board[y][x] = Board.HURT

    if hide:
      for y in range(self.h):
        for x in range(self.w):
          if board[y][x] == Board.SHIP:
            board[y][x] = Board.EMPTY

    return board


  def draw(
    self,
    screen,
    y:     int,
    x:     int,
    shots: [(int, int)],
    hide:  bool = False
  ):
    hsl = len(str(self.h))
    screen.addstr(
      y, x, ' ' + ' ' * hsl + ' '.join(Board.HORIZONTAL_SIGNS[:self.w]) + ' '
    )
    screen.addstr(
        y+1, x, ' ' * hsl + Board.TOPLEFT +
              Board.HORIZONTAL * (self.w * 2 - 1) + Board.TOPRIGHT
    )

    board = self._translate_board(shots, hide)
    for yy in range(self.h):
      screen.addstr(y+2+yy, x, '%*i' % (hsl, yy+1) + Board.VERTICAL)
      if Board.HURT not in board[yy]:
        screen.addstr(y+2+yy, x+hsl+1, ' '.join(board[yy]))
      else:
        for xx in range(self.w):
          if board[yy][xx] == Board.HURT and self._is_kill(board, yy, xx):
            screen.addch(
              y+2+yy, x+hsl+1+xx*2,
              board[yy][xx],
              curses.color_pair(Color.RED)
            )
          else:
            screen.addch(y+2+yy, x+hsl+1+xx*2, board[yy][xx])
      screen.addstr(y+2+yy, x+hsl+self.w*2, Board.VERTICAL)

    screen.addstr(
      y+2+self.h, x, ' ' * hsl + Board.DOWNLEFT +
            Board.HORIZONTAL * (self.w * 2 - 1) + Board.DOWNRIGHT 
    )
    return


  def tostr(self, shots: [(int, int)], hide: bool = False):
    return '\n'.join(
      [ ' ' + ' ' * hsl + ' '.join(Board.HORIZONTAL_SIGNS[:self.w]) + ' '] +
      [ ' ' * hsl + Board.TOPLEFT + Board.HORIZONTAL * (self.w * 2 - 1) + Board.TOPRIGHT ] +
      [ '%*i' % (hsl, y) + Board.VERTICAL + ' '.join(self._d[y-1]) + Board.VERTICAL
        for y in range(1, self.h+1) ] +
      [ ' ' * hsl + Board.DOWNLEFT + Board.HORIZONTAL * (self.w * 2 - 1) + Board.DOWNRIGHT ]
    )


  def required_size(self):
    return self.h + 3, len(str(self.h)) + self.w * 2 + 2


  def board2screen(
    self,
    y: int, x: int,
    winy: int = 0, winx: int = 0
  ) -> (int, int):
    return y + 2 + winy, x*2 + len(str(self.h)) + 1 + winx
