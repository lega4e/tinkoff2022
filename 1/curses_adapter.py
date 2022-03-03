import curses


class Color:
    KILL = 1
    CURSOR = 2


class CursesAdapter:
    def __init__(self):
        self._curses = curses
        self._screen = curses.initscr()
        self._curses.cbreak()
        self.init_colors()

    def init_colors(self):
        self._curses.start_color()
        self._curses.init_pair(
            Color.KILL, self._curses.COLOR_RED, self._curses.COLOR_BLACK
        )
        self._curses.init_pair(
            Color.CURSOR, self._curses.COLOR_BLACK, self._curses.COLOR_YELLOW
        )

    def get_screen(self):
        return self._screen

    def get_curses(self):
        return self._curses

    def game_mode(self):
        self._curses.noecho()
        self._curses.curs_set(0)

    def command_mode(self):
        self._curses.echo()
        self._curses.curs_set(1)

    def quit(self):
        self._curses.endwin()
