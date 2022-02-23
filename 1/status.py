import copy
import curses

from ship import Ship



def find_if(l: [], key):
  for el in l:
    if key(el):
      return el
  return None


class Status:
  SHIP = '■'
  HURT = 'X'

  def __init__(self, w: int, ships: [ Ship ]):
    self.w = w
    self.ships = sorted(ships, key=lambda x: x.l, reverse=True)
    

  def tostr(self) -> [ str ]:
    if max(map(lambda x: x.l, self.ships)) > self.w:
      raise Exception("Status width too small")

    lines = ['']
    ships = copy.deepcopy(self.ships)
    while len(ships) != 0:
      w = self.w - len(lines[-1]) - (1 if len(lines[-1]) != 0 else 0)
      ship = find_if(ships, lambda ship: ship.l <= w)
      if ship is not None:
        lines[-1] += (
          (' ' if len(lines[-1]) != 0 else '') +
          (Status.SHIP if ship.live else Status.HURT) * ship.l
        )
        ships.remove(ship)
        print(ships)
      else:
        lines.append('')
    return lines


  def required_size(self):
    return len(self.tostr()), self.w
