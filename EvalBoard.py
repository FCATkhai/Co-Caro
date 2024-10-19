import numpy as np


class EvalBoard:
    def __init__(self, size=20) -> None:
        self.size = size
        self.evaluationBoard = 0
        self.EBoard = np.zeros((size, size), dtype=int)

    def resetBoard(self):
        for row in range(self.size):
            for col in range(self.size):
                self.EBoard[row][col] = 0

    def setPosition(self, row, col, diem):
        self.EBoard[row][col] = diem

    def maxPos(self):
        max = 0  # diem max
        point = (-1, -1)
        for row in range(self.size):
            for col in range(self.size):
                if self.EBoard[row][col] > max:
                    max = self.EBoard[row][col]
                    point = (row, col)
        if max == 0:
            return None
        self.evaluationBoard = max
        return point
