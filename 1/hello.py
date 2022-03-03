class Hello:
    def __init__(self, h, w):
        self.hello = "Welcome to the sea battle game"
        self.prompt = "Tap Enter to start (%ix%i)" % (w, h)
        pass

    def required_size(self) -> (int, int):
        return 2, max(len(self.hello), len(self.prompt))

    def tostr(self, h, w) -> str:
        lines = [""] * h
        if h < 8:
            lines[0] = self.hello.center(w, " ")
        else:
            lines[1] = self.hello.center(w, " ")
        lines[h // 2] = self.prompt.center(w, " ")
        return "\n".join(lines)
