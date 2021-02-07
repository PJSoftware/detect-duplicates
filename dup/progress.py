class Bar:
    """provides progress bar for terminal"""

    prefix = "Progress"
    suffix = ""
    width = 40
    status = 0
    threshold = 100
    step = 0

    def __init__(self, prefix: str, width: int, threshold: int, suffix: str = ""):
        self.prefix = prefix
        self.width = width
        self.threshold = threshold
        self.suffix = suffix
        self.status = 0
        self.step = 0

    def __repr__(self):
        if self.status > self.threshold:
            self.threshold = self.status
        if self.threshold > 0:
            bar_done = int(self.width * self.status/self.threshold)
            pc = int(1000 * self.status/self.threshold) / 10
            bar_remain = self.width - bar_done
            bar = "#"*bar_done + " "*bar_remain
            return f"\r{self.prefix}: [{bar}] {pc}% {self.suffix}"
        else:
            self.step += 1
            if self.step > self.width:
                pos = self.width*2 - self.step
            else:
                pos = self.step
            bar_l = " " * (pos-1)
            bar_r = " " * (self.width - pos)
            bar = bar_l + "#" + bar_r
            if self.step == (self.width-1)*2:
                self.step = 0
            return f"\r{self.prefix}: [{bar}] {self.suffix}"

    def update(self, status: int = 0, suffix: str = ""):
        if suffix != "":
            self.suffix = suffix
        if status > self.status:
            self.status = status
        bar = self.__repr__()
        print(f"\r{bar}", end="")
    
    def close(self):
        print("\n")
