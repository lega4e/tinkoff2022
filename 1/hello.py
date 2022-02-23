from utils import centered_str


class Hello:
    def __init__(self, h, w):
        self.hello = "Welcome to the sea battle game"
        self.prompt = "Tap Enter to start (%ix%i)" % (w, h)
        pass

    def required_size(self):
        return 2, max(len(self.hello), len(self.prompt))

    def tostr(self, h, w):
        lines = [""] * h
        if h < 8:
            lines[0] = centered_str(self.hello, w)
        else:
            lines[1] = centered_str(self.hello, w)
        lines[h // 2] = centered_str(self.prompt, w)
        return "\n".join(lines)
