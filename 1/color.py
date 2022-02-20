import curses

class Color:
  RED = 1

def init_colors():
  curses.start_color()
  curses.init_pair(Color.RED, curses.COLOR_RED, curses.COLOR_BLACK)
