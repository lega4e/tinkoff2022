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
  MAX_W = len(HORIZONTAL_SIGNS)
  SHIP_SYM = '■'


  def __init__(self, h: int, w: int, ships: [ int ] = None):
    self.w = w
    self.h = h
    if ships is not None:
      self.arrange_ships(ships)
    else:
      self.clear()


  def clear(self):
    self._d = [ [' '] * self.w for i in range(self.h) ]


  def check_ship(self, y: int, x: int, hor: bool, ship: int) -> bool:
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
        if self._d[yy][xx] != ' ':
          return False

    return True


  def place_ship(self, y: int, x: int, hor: bool, ship: int):
    if hor:
      for xx in range(x, x+ship):
        self._d[y][xx] = Board.SHIP_SYM
    else:
      for yy in range(y, y+ship):
        self._d[yy][x] = Board.SHIP_SYM


  def _arrange_ship(self, ship: int) -> bool:
    for i in range(20):
      y, x = randint(0, self.h-1), randint(0, self.w-1)
      hor = randint(0, 1)
      if self.check_ship(y, x, hor, ship):
        self.place_ship(y, x, hor, ship)
        return True
    return False


  def arrange_ships(self, ships: [ int ]):
    self.ships = sorted(ships, reverse=True)
    self.clear()
    for i in range(100):
      if all([ self._arrange_ship(ship) for ship in self.ships ]):
        return True
    raise Exception("Error: can't arrange ships; try to increase board size")


  def tostr(self):
    return '\n'.join(
      [ ' ' * len(str(self.h)) +
        ' '.join(Board.HORIZONTAL_SIGNS[:self.w]) ] +
      [ '%*i' % (len(str(self.h)), y) + ' '.join(self._d[y-1])
        for y in range(1, self.h+1) ]
    )


  def required_size(self):
    return self.h + 1, len(str(self.h)) + self.w * 2
