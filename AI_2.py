import copy
import math
from CalculateScore import evaluateBoard

class AI:
    def __init__(self, player=2):  # Số đại diện cho AI (thường là 2)
        self.AI = player
        self.opponent = 3 - player  # Số đại diện cho đối thủ (thường là 1)
        self.maxDepth = 2  # Độ sâu tối đa trên cây tìm kiếm

    def find_best_move(self, board, depth):
        best_move = None
        best_value = -math.inf
        for move in self.generate_moves(board, 2):
            temp_board = copy.deepcopy(board)
            temp_board.setPosition(move[0], move[1], self.AI)
            move_value = self.alpha_beta(temp_board, depth - 1, -math.inf, math.inf, True)
            temp_board.setPosition(move[0], move[1], 0)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        print("max score: ", best_value)
        return best_move

    def alpha_beta(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.game_over(board):
            return evaluateBoard(board, self.AI if maximizingPlayer else self.opponent)

        if maximizingPlayer:
            max_eval = -math.inf
            for move in self.generate_moves(board, 2):
                temp_board = copy.deepcopy(board)
                temp_board.setPosition(move[0], move[1], self.AI)
                eval = self.alpha_beta(temp_board, depth - 1, alpha, beta, False)
                temp_board.setPosition(move[0], move[1], 0)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.generate_moves(board, 2):
                temp_board = copy.deepcopy(board)
                temp_board.setPosition(move[0], move[1], self.AI)
                eval = self.alpha_beta(temp_board, depth - 1, alpha, beta, True)
                temp_board.setPosition(move[0], move[1], 0)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def generate_moves(self, board, area):
        N = board.size  # Kích thước của bàn cờ
        moves = set()  # Dùng tập hợp để tránh các ô trùng lặp

        # Duyệt qua bàn cờ để tìm các ô có quân cờ
        for row in range(N):
            for col in range(N):
                if board.getPosition(row, col) != 0:  # Giả sử 0 là ô trống
                    # Tìm các ô trống trong vùng 2 ô xung quanh
                    for i in range(-area, area + 1):  # Duyệt từ -2 đến 2
                        for j in range(-area, area + 1):
                            new_row, new_col = row + i, col + j
                            # Kiểm tra xem tọa độ có nằm trong bàn cờ không
                            if 0 <= new_row < N and 0 <= new_col < N:
                                # Chỉ thêm ô nếu nó trống
                                if board.getPosition(new_row, new_col) == 0:
                                    moves.add((new_row, new_col))

        # Trả về danh sách các ô trống trong vùng 2 ô xung quanh các ô đã có quân cờ
        return list(moves)

    def game_over(self, boardState):
        for row in range(boardState.size):
            for col in range(boardState.size):
                if boardState.getPosition(row, col) != 0:
                    if boardState.final_state(row, col) != 0:
                        return True
        return False

    def AI_move(self, boardState):
        move = self.find_best_move(boardState, 1)
        return move
