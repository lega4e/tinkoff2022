class CmdLine:
    def __init__(self):
        self.prompt = "Type ':' to enter command line"
        self.hint = "Commands: quit, save <name>, load <name>"

    def required_size(self):
        return 1, max(len(self.prompt), int(len(self.hint) * 1.5))

    def tostr_prompt(self, h, w):
        lines = [""] * h
        lines[-1] = self.prompt.rjust(w, ' ')
        return "\n".join(lines)

    def tostr_hint(self, h, w):
        lines = [""] * h
        lines[-1] = ":" + self.hint.rjust(w - 1, ' ')
        return "\n".join(lines)

    def answer(self, h, w, ans):
        lines = [""] * h
        lines[-1] = " " + ans.ljust(w - 1, ' ')
        return "\n".join(lines)
