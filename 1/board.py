import copy
import curses

from color  import Color
from random import randint


def get_probs_val(weights: dict):
  choice = randint(1, sum(weights.keys()))
  for key, value in weights.items():
    choice -= value
    if choice <= 0:
      return key
  raise Exception("Weights out of range")


def generate_ships(h: int, w: int):
  weights = dict()
  val = 1

  for l in range(min(7, w-1, h-1), 0, -1):
    weights[l] = val
    val += 1

  sqrt = (w * h) ** 0.5
  k = randint(int(sqrt * 1.8), int(sqrt * 2.2))
  ships = []

  while k > 0:
    ship = get_probs_val(weights)
    if ship > k:
      continue
    k -= ship
    ships.append(ship)

  return sorted(ships)



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


  def __init__(self, h: int, w: int, ships: [ int ] = None):
    self.w = w
    self.h = h
    if ships is not None:
      self.arrange_ships(ships)
    else:
      self.clear()


  def clear(self):
    self._d = [ [Board.EMPTY] * self.w for i in range(self.h) ]


  def arrange_ships(self, ships: [ int ]):
    self.ships = sorted(ships, reverse=True)
    self.clear()
    for i in range(1000):
      if all([ self._arrange_ship(ship) for ship in self.ships ]):
        return True
    raise Exception("Error: can't arrange ships; try to increase board size")


  def _check_ship(self, y: int, x: int, hor: bool, ship: int) -> bool:
    my = y if hor else y + ship - 1
    mx = x if not hor else x + ship - 1
    if x < 0 or mx >= self.w or y < 0 or my >= self.h:
      return False

    for yy in range(y-1, my+2):
      if yy >= self.h:
        break
      for xx in range(x-1, mx+2):
        if xx >= self.w:
          break
        if self._d[yy][xx] != Board.EMPTY:
          return False

    return True


  def _place_ship(self, y: int, x: int, hor: bool, ship: int):
    if hor:
      for xx in range(x, x+ship):
        self._d[y][xx] = Board.SHIP
    else:
      for yy in range(y, y+ship):
        self._d[yy][x] = Board.SHIP


  def _arrange_ship(self, ship: int) -> bool:
    for i in range(50):
      y, x = randint(0, self.h-1), randint(0, self.w-1)
      hor = randint(0, 1)
      if self._check_ship(y, x, hor, ship):
        self._place_ship(y, x, hor, ship)
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
