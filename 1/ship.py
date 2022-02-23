from random import randint


class Ship:
    def __init__(self, y: int, x: int, l: int, hor: bool, live: bool):
        self.y = y
        self.x = x
        self.l = l
        self.hor = hor
        self.live = live

    def points(self):
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

    def bounds(self):
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


def generate_ships(h: int, w: int):
    "Сгенерировать корабли в соответствии с размерами поля"
    weights = dict()
    val = 1

    for l in range(min(7, w - 1, h - 1), 0, -1):
        weights[l] = val
        val += 1

    sqrt = (w * h) ** 0.5
    k = randint(int(sqrt * 1.8), int(sqrt * 2.2))
    ships = []

    while k > 0:
        ship = _get_probs_val(weights)
        if ship > k:
            continue
        k -= ship
        ships.append(ship)

    return map(lambda l: Ship(0, 0, l, True, True), sorted(ships, reverse=True))
