import numpy

class pos2:
    def __init__(self, x: int = 0, y: int = 0, dtype = object) -> None:
        self.dtype = dtype
        self.x = x
        self.y = y
    def getVector(self) -> numpy.array:
        return numpy.array([self.x, self.y], dtype = self.dtype)
    def __repr__(self) -> str: return f"pos2 [{self.x}, {self.y}]"

class size2:
    def __init__(self, w: int = 0, h: int = 0, dtype = object) -> None:
        self.dtype = dtype
        self.w = w
        self.h = h
    def getVector(self) -> numpy.array:
        return numpy.array([self.w, self.h], dtype = self.dtype)
    def __repr__(self) -> str: return f"size2 [{self.w}, {self.h}]"
