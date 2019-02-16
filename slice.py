class Slice:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def cords(self):
        return f"{self.y1} {self.x1} {self.y2} {self.x2}"

    def __str__(self):
        return self.cords

    def __repr__(self):
        return self.cords