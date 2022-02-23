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


  def __init__(self, h: int, w: int, ships: [ Ship ] = []):
    self.w = w
    self.h = h
    if ships is not None:
      self.arrange_ships(ships)
    else:
      self.clear()
    self.shots = []


  def clear(self):
    'Очистить поле полностью, в том числе корабли'
    self._d = [ [Board.EMPTY] * self.w for i in range(self.h) ]
    self.ships = []
    self.shots = []


  def clear_shots(self):
    'Удалить все выстрелы'
    self.shots = []
    for ship in self.ships:
      ship.live = True


  def shot(self, y: int, x: int):
    'Выстрелить по клетке'
    self.shots.append((y, x))
    for ship in self.ships:
      if (y, x) not in ship:
        continue
      if all(map(lambda p: p in self.shots, ship.points())):
        ship.live = False
        self._round_ship(ship)


  def arrange_ships(self, ships: [ Ship ]):
    'Расставить переданные корабли'
    self.ships = sorted(ships, key=lambda s: s.l, reverse=True)

    self.clear()
    for i in range(1000):
      if all([ self._arrange_ship(ship) for ship in self.ships ]):
        return
    raise Exception("Error: can't arrange ships; try to increase board size")


  def draw(
    self,
    screen,
    y:     int,
    x:     int,
    hide:  bool = False
  ):
    'Отрисовать поле на экране screen в точке (y, x)'
    hsl = len(str(self.h))
    screen.addstr(
      y, x, ' ' + ' ' * hsl + ' '.join(Board.HORIZONTAL_SIGNS[:self.w]) + ' '
    )
    screen.addstr(
        y+1, x, ' ' * hsl + Board.TOPLEFT +
              Board.HORIZONTAL * (self.w * 2 - 1) + Board.TOPRIGHT
    )

    board = self._translate_board(hide)
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


  def required_size(self):
    'Вернуть требуемый для корректной отрисовки размер'
    return self.h + 3, len(str(self.h)) + self.w * 2 + 2


  def board2screen(
    self,
    y: int, x: int,
    winy: int = 0, winx: int = 0
  ) -> (int, int):
    'Отобразить координаты доски на координаты окна, которое может быть смещено'
    return y + 2 + winy, x*2 + len(str(self.h)) + 1 + winx


  def isover(self):
    'Провеить, что все коробли убиты'
    return all(map(lambda ship: not ship.live, self.ships))


  def _round_ship(self, ship: Ship):
    self.shots.extend(filter(
      lambda p: p[0] >= 0 and p[0] < self.h and p[1] >= 0 and p[1] < self.w,
      ship.bounds()
    ))


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
    for y, x in ship.points():
      self._d[y][x] = Board.SHIP


  def _arrange_ship(self, ship: Ship) -> bool:
    for i in range(self.w * self.h):
      ship.y, ship.x = randint(0, self.h-1), randint(0, self.w-1)
      ship.hor = randint(0, 1)
      if self._check_ship(ship):
        self._place_ship(ship)
        return True
    return False


  def _is_kill(self, board, y, x):
    for ship in self.ships:
      if (y, x) in ship:
        return not ship.live
    return False


  def _translate_board(self, hide):
    board = copy.deepcopy(self._d)
    for y, x in self.shots:
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
