class Bar:
    """provides progress bar for terminal"""

    prefix = "Progress"
    suffix = ""
    width = 40
    status = 0
    threshold = 100

    def __init__(self, prefix: str, width: int, threshold: int, suffix: str = ""):
        self.prefix = prefix
        self.width = width
        self.threshold = threshold
        self.suffix = suffix
        self.status = 0

    def __repr__(self):
        if self.status > self.threshold:
            self.threshold = self.status
        bar_done = int(self.width * self.status/self.threshold)
        pc = int(1000 * self.status/self.threshold) / 10
        bar_remain = self.width - bar_done
        bar = "#"*bar_done + " "*bar_remain
        return f"\r{self.prefix}: [{bar}] {pc}% {self.suffix}"

    def update(self, status: int, suffix: str = ""):
        if suffix != "":
            self.suffix = suffix
        self.status = status
        bar = self.__repr__()
        print(f"\r{bar}", end="")
