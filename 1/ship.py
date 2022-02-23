from random import randint


class Ship:
  def __init__(self, y: int, x: int, l: int, hor: bool, live: bool):
    self.y = y
    self.x = x
    self.l = l
    self.hor = hor
    self.live = live


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

  return map(lambda l: Ship(0, 0, l, True, True), sorted(ships, reverse=True))
