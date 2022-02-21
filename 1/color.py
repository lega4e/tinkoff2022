import curses

class Color:
  RED = 1
  CURSOR = 2

def init_colors():
  curses.start_color()
  curses.init_pair(Color.RED, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(Color.CURSOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
