from utils import righted_str

class CmdLine:
  def __init__(self):
    self.prompt = "Type ':' to enter command line"
    self.hint   = 'Commands: quit, save <name>, load <name>'

  def required_size(self):
    return 1, max(len(self.prompt), int(len(self.hint) * 1.5))
  
  def tostr_prompt(self, h, w):
    lines = [''] * h
    lines[-1] = righted_str(self.prompt, w)
    return '\n'.join(lines)

  def tostr_hint(self, h, w):
    lines = [''] * h
    lines[-1] = ':' + righted_str(self.hint, w-1)
    return '\n'.join(lines)
