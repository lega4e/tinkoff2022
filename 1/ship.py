from random import randint


class Ship:
    def __init__(self, y: int, x: int, l: int, hor: bool, live: bool):
        self.y = y
        self.x = x
        self.l = l
        self.hor = hor
        self.live = live

    def points(self) -> (int, int):
        "Итератор по всем клеткам, в которых есть корабль"
        y, x, = (
            self.y,
            self.x,
        )
        for i in range(self.l):
            yield y, x
            if self.hor:
                x += 1
            else:
                y += 1

    def bounds(self) -> (int, int):
        "Итератор по всем клеткам в окресности корабля"
        if self.hor:
            for x in range(self.x - 1, self.x + self.l + 1):
                yield self.y - 1, x
            yield self.y, self.x - 1
            yield self.y, self.x + self.l
            for x in range(self.x - 1, self.x + self.l + 1):
                yield self.y + 1, x
        else:
            for y in range(self.y - 1, self.y + self.l + 1):
                yield y, self.x - 1
            yield self.y - 1, self.x
            yield self.y + self.l, self.x
            for y in range(self.y - 1, self.y + self.l + 1):
                yield y, self.x + 1

    def __contains__(self, p: (int, int)) -> bool:
        y, x = p
        return (
            y == self.y and self.x <= x < self.x + self.l
            if self.hor
            else x == self.x and self.y <= y < self.y + self.l
        )


def _get_probs_val(weights: dict):
    choice = randint(1, sum(weights.keys()))
    for key, value in weights.items():
        choice -= value
        if choice <= 0:
            return key
    raise Exception("Weights out of range")


DENSITY = 0.2


def generate_ships(h: int, w: int) -> [Ship]:
    "Сгенерировать корабли в соответствии с размерами поля"
    ship_cell_count = max(int(w * h * DENSITY), 1)
    longest_ship = 0
    ships = []
    while ship_cell_count > 0:
        for i in range(1, longest_ship + 2):
            if ship_cell_count - i >= 0:
                ships.append(i)
                ship_cell_count -= i
                longest_ship = max(longest_ship, i)
            else:
                break
    return list(map(lambda ship: Ship(0, 0, ship, True, True), ships))
