import copy
from EvalBoard import EvalBoard

class AI:
    def __init__(self, player=2):  # Số đại diện cho AI (thường là 2)
        self.AI = player
        self.opponent = 3 - player  # Số đại diện cho đối thủ (thường là 1)
        self.eBoard = EvalBoard()
        self.AScore = [0, 4, 27, 256, 1458]  # Bảng điểm tấn công
        self.DScore = [0, 2, 9, 99, 769]  # Bảng điểm phòng thủ
        self.maxDepth = 4  # Độ sâu tối đa trên cây tìm kiếm
        self.maxMove = 4  # Số con tối đa trên cây tìm kiếm
        self.goPoint = None  # Vị trí AI sẽ đánh

    # Tạo bảng điểm đánh giá
    def evalChessBoard(self, player, boardState, eBoard):
        eBoard.resetBoard()
        # Duyet theo hang
        for row in range(eBoard.size):
            for col in range(eBoard.size - 4):
                eAI = 0  # so quan AI
                eHuman = 0  # so quan Human
                for i in range(5):
                    if boardState.getPosition(row, col + i) == self.opponent:  # neu quan do la cua human
                        eHuman += 1  # tang so quan human
                    if boardState.getPosition(row, col + i) == self.AI:  # neu quan do la cua AI
                        eAI += 1  # tang so quan PC

                # Trong vong 5 o khong co quan dich
                if eHuman * eAI == 0 and eHuman != eAI:
                    for i in range(5):
                        if boardState.getPosition(row, col + i) == 0:  # neu o chua danh
                            if eHuman == 0:  # eAI khac 0
                                if player == self.opponent:
                                    eBoard.EBoard[row][col + i] += self.DScore[eAI]  # cho diem phong ngu
                                else:
                                    eBoard.EBoard[row][col + i] += self.AScore[eAI]  # cho diem tan cong
                            if eAI == 0:  # eHuman khac 0
                                if player == self.AI:
                                    eBoard.EBoard[row][col + i] += self.DScore[eHuman]  # cho diem phong ngu
                                else:
                                    eBoard.EBoard[row][col + i] += self.AScore[eHuman]  # cho diem tan cong
                            if eHuman == 4 or eAI == 4:  # Human hoac AI sap chien thang
                                eBoard.EBoard[row][col + i] *= 2

        # Duyet theo cot
        for col in range(eBoard.size):
            for row in range(eBoard.size - 4):
                eAI = 0
                eHuman = 0
                for i in range(5):
                    if boardState.getPosition(row + i, col) == 1:
                        eHuman += 1
                    if boardState.getPosition(row + i, col) == 2:
                        eAI += 1
                if eHuman * eAI == 0 and eHuman != eAI:
                    for i in range(5):
                        if boardState.getPosition(row + i, col) == 0:  # Neu o chua duoc danh
                            if eHuman == 0:
                                if player == self.opponent:
                                    eBoard.EBoard[row + i][col] += self.DScore[eAI]
                                else:
                                    eBoard.EBoard[row + i][col] += self.AScore[eAI]
                            if eAI == 0:
                                if player == self.AI:
                                    eBoard.EBoard[row + i][col] += self.DScore[eHuman]
                                else:
                                    eBoard.EBoard[row + i][col] += self.AScore[eHuman]
                            if eHuman == 4 or eAI == 4:
                                eBoard.EBoard[row + i][col] *= 2

        # Duyet theo duong cheo thuan \ (cheo xuong)
        for col in range(eBoard.size - 4):
            for row in range(eBoard.size - 4):
                eAI = 0
                eHuman = 0
                for i in range(5):
                    if boardState.getPosition(row + i, col + i) == self.opponent:
                        eHuman += 1
                    if boardState.getPosition(row + i, col + i) == self.AI:
                        eAI += 1
                if eHuman * eAI == 0 and eHuman != eAI:
                    for i in range(5):
                        if boardState.getPosition(row + i, col + i) == 0:  # Neu o chua duoc danh
                            if eHuman == 0:
                                if player == self.opponent:
                                    eBoard.EBoard[row + i][col + i] += self.DScore[eAI]
                                else:
                                    eBoard.EBoard[row + i][col + i] += self.AScore[eAI]
                            if eAI == 0:
                                if player == self.AI:
                                    eBoard.EBoard[row + i][col + i] += self.DScore[eHuman]
                                else:
                                    eBoard.EBoard[row + i][col + i] += self.AScore[eHuman]
                            if eHuman == 4 or eAI == 4:
                                eBoard.EBoard[row + i][col + i] *= 2

        # Duyet theo duong cheo nghich / (cheo len)
        for row in range(4, eBoard.size):
            for col in range(eBoard.size - 4):
                eAI = 0
                eHuman = 0
                for i in range(5):
                    if boardState.getPosition(row - i, col + i) == self.opponent:
                        eHuman += 1
                    if boardState.getPosition(row - i, col + i) == self.AI:
                        eAI += 1
                if eHuman * eAI == 0 and eHuman != eAI:
                    for i in range(5):
                        if boardState.getPosition(row - i, col + i) == 0:  # neu o chua duoc danh
                            if eHuman == 0:
                                if player == self.opponent:
                                    eBoard.EBoard[row - i][col + i] += self.DScore[eAI]
                                else:
                                    eBoard.EBoard[row - i][col + i] += self.AScore[eAI]
                            if eAI == 0:
                                if player == self.AI:
                                    eBoard.EBoard[row - i][col + i] += self.DScore[eHuman]
                                else:
                                    eBoard.EBoard[row - i][col + i] += self.AScore[eHuman]
                            if eHuman == 4 or eAI == 4:
                                eBoard.EBoard[row - i][col + i] *= 2

    def alphaBeta(self, boardState, alpha, beta, depth, player):
        if player == self.AI:
            self.maxValue(boardState, alpha, beta, depth)
        else:
            self.minValue(boardState, alpha, beta, depth)

    def maxValue(self, boardState, alpha, beta, depth):
        self.eBoard.maxPos()
        value = self.eBoard.evaluationBoard
        if depth >= self.maxDepth:
            return value

        self.evalChessBoard(player=self.AI, boardState=boardState, eBoard=self.eBoard)  # Cập nhật bảng đánh giá
        # Tìm những nút con có khả năng đánh cao nhất
        childList = []
        for i in range(self.maxMove):
            point = self.eBoard.maxPos()
            if point is None:
                break
            childList.append(point)
            self.eBoard.setPosition(point[0], point[1], 0)

        v = float('-inf')
        for point in childList:
            temp_board = copy.deepcopy(boardState)
            temp_board.setPosition(point[0], point[1], self.AI)
            v = max(v, self.minValue(temp_board, alpha, beta, depth + 1))
            temp_board.setPosition(point[0], point[1], 0)
            if v >= beta or boardState.final_state(point[0], point[1]) == self.AI:
                self.goPoint = point
                return v  # cắt tỉa alpha
            alpha = max(alpha, v)

        return v

    def minValue(self, boardState, alpha, beta, depth):
        self.eBoard.maxPos()
        value = self.eBoard.evaluationBoard
        if depth >= self.maxDepth:
            return value

        self.evalChessBoard(player=self.opponent, boardState=boardState, eBoard=self.eBoard)  # Cập nhật bảng đánh giá
        # Tìm những nút con có khả năng đánh cao nhất
        childList = []
        for i in range(self.maxMove):
            point = self.eBoard.maxPos()
            if point is None:
                break
            childList.append(point)
            self.eBoard.setPosition(point[0], point[1], 0)

        v = float('inf')
        for point in childList:
            temp_board = copy.deepcopy(boardState)
            temp_board.setPosition(point[0], point[1], self.opponent)
            v = min(v, self.maxValue(temp_board, alpha, beta, depth + 1))
            temp_board.setPosition(point[0], point[1], 0)
            if v <= alpha or boardState.final_state(point[0], point[1]) == self.opponent:
                self.goPoint = point
                return v  # cắt tỉa beta
            beta = min(beta, v)

        return v

    def AI_move(self, boardState):
        self.goPoint = None
        self.alphaBeta(boardState, 0, 1, 0, self.AI)
        return self.goPoint
