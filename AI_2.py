import copy
from EvalBoard import EvalBoard
from CalculateScore import *


class AI:
    def __init__(self, player=2):  # Số đại diện cho AI (thường là 2)
        self.AI = player
        self.opponent = 3 - player  # Số đại diện cho đối thủ (thường là 1)
        self.eBoard = EvalBoard()
        self.AScore = [0, 4, 27, 256, 1458]  # Bảng điểm tấn công
        self.DScore = [0, 2, 9, 99, 769]  # Bảng điểm phòng thủ
        self.maxDepth = 2  # Độ sâu tối đa trên cây tìm kiếm
        self.maxMove = 4  # Số con tối đa trên cây tìm kiếm
        self.goPoint = None  # Vị trí AI sẽ đánh
        self.scoreSet = set()

    def alphaBeta(self, boardState, depth, alpha, beta, maximizing):
        # Điều kiện dừng: đạt độ sâu 0, bàn cờ đầy
        if depth == self.maxDepth or boardState.is_full():
            temp_board = copy.deepcopy(boardState)
            score = evaluateBoard(temp_board)
            print(score)
            self.scoreSet.add(score)
            return score, None

        empty_sqrs = boardState.get_empty_sqrs()
        # Sắp xếp các nước đi theo thứ tự ưu tiên để cắt tỉa alpha-beta hiệu quả hơn
        empty_sqrs.sort(key=lambda move: self.move_ordering_score(boardState, move[0], move[1]), reverse=maximizing)

        if maximizing:
            max_eval = -float('inf')
            best_move = None
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(boardState)
                temp_board.setPosition(row, col, self.AI)
                eval, _ = self.alphaBeta(temp_board, depth + 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Cắt tỉa alpha
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(boardState)
                temp_board.setPosition(row, col, self.opponent)
                eval, _ = self.alphaBeta(temp_board, depth + 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Cắt tỉa beta
            return min_eval, best_move

    # --------------------------------------------------------
    def evaluate_board_1(self, board):
        score = 0
        if self.check_win(board, self.AI):
            score += 10000
        if self.check_win(board, self.opponent):
            score -= 10000
        for row in range(board.size):
            for col in range(board.size):
                if board.squares[row][col] == self.AI:
                    score += self.evaluate_position(board, row, col, self.AI)
                elif board.squares[row][col] == self.opponent:
                    score -= self.evaluate_position(board, row, col, self.opponent)
        return score

    def evaluate_position(self, board, row, col, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            block_count = 0
            for delta in range(-3, 4):
                r = row + delta * dr
                c = col + delta * dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    if board.squares[r][c] == player:
                        count += 1
                    elif board.squares[r][c] != 0:
                        block_count += 1
                        break
                else:
                    block_count += 1
                    break
            if block_count < 2:
                score += count ** 2
        return score

    def check_win(self, boardState, player):
        for row in range(boardState.size):
            for col in range(boardState.size):
                if boardState.squares[row][col] == player:
                    if boardState.final_state(row, col) == player:
                        return True
        return False

    def move_ordering_score(self, board, row, col):
        score = 0
        center = board.size // 2
        # Ưu tiên các nước đi gần trung tâm
        score += 10 - (abs(row - center) + abs(col - center))

        # Prioritize moves that form or block potential advantages (Ưu tiên các nước đi tạo ra hoặc chặn các lợi thế tiềm năng)
        temp_board = copy.deepcopy(board)
        temp_board.setPosition(row, col, self.AI)
        score += self.evaluate_potential_advantages(temp_board, self.AI)

        temp_board = copy.deepcopy(board)
        temp_board.setPosition(row, col, self.opponent)
        score += self.evaluate_potential_advantages(temp_board, self.opponent)

        return score

    def evaluate_potential_advantages(self, board, player):
        score = 0
        opponent = 3 - player
        for row in range(board.size):
            for col in range(board.size):
                if board.squares[row][col] == 0:
                    score += self.evaluate_future_sequence(board, row, col, player)
                    score -= self.evaluate_future_sequence(board, row, col, opponent)
        return score

    def evaluate_future_sequence(self, board, row, col, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = self.get_line(board, row, col, dr, dc)
            score += self.score_potential_sequence(line, player, board.max_item_win)
        return score

    def score_potential_sequence(self, line, player, max_win):
        score = 0
        opponent = 3 - player
        player_count = line.count(player)
        empty_count = line.count(0)

        if player_count == max_win - 2 and empty_count == 2:
            score += 50  # Potential future advantage
        elif player_count == max_win - 3 and empty_count == 3:
            score += 10  # Developing sequence

        return score

    def get_line(self, board, row, col, dr, dc):
        # Lấy một dòng các ô từ vị trí (row, col) theo hướng (dr, dc)
        line = []
        for i in range(-board.max_item_win + 1, board.max_item_win):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < board.size and 0 <= c < board.size:
                line.append(board.squares[r][c])
            else:
                break
        return line
    #--------------------------------------------------------------------------
    def evaluate_board(self, board, player):
        max_score = self.calculate_paths(board, self.AI)
        min_score = self.calculate_paths(board, self.opponent)

        if player == self.AI:
            return max_score - min_score
        else:
            return min_score - max_score

    def calculate_paths(self, board, player):
        score = 0
        # Trọng số cho từng độ dài chuỗi quân liên tiếp
        weights = {2: 1, 3: 5, 4: 50, 5: 1000}  # Chuỗi 5 quân nghĩa là thắng

        for sequence in self.find_sequences(board, player):
            length = len(sequence)  # Độ dài chuỗi liên tiếp của quân `player`
            if length in weights:
                score += weights[length]

        return score

    def find_sequences(self, board, player):
        sequences = []  # Danh sách lưu trữ tất cả các chuỗi liên tiếp của quân player
        N = len(board)  # Kích thước của bàn cờ N x N

        # Kiểm tra các chuỗi liên tiếp theo hàng ngang
        for row in range(N):
            count = 0
            current_sequence = []
            for col in range(N):
                if board[row][col] == player:
                    current_sequence.append((row, col))
                    count += 1
                else:
                    if count > 1:
                        sequences.append(current_sequence)
                    count = 0
                    current_sequence = []
            if count > 1:
                sequences.append(current_sequence)

        # Kiểm tra các chuỗi liên tiếp theo hàng dọc
        for col in range(N):
            count = 0
            current_sequence = []
            for row in range(N):
                if board[row][col] == player:
                    current_sequence.append((row, col))
                    count += 1
                else:
                    if count > 1:
                        sequences.append(current_sequence)
                    count = 0
                    current_sequence = []
            if count > 1:
                sequences.append(current_sequence)

        # Kiểm tra các chuỗi liên tiếp theo đường chéo từ trái sang phải
        for start in range(-N + 1, N):  # Duyệt qua các đường chéo chính và phụ
            count = 0
            current_sequence = []
            for row in range(N):
                col = row + start
                if 0 <= col < N:
                    if board[row][col] == player:
                        current_sequence.append((row, col))
                        count += 1
                    else:
                        if count > 1:
                            sequences.append(current_sequence)
                        count = 0
                        current_sequence = []
            if count > 1:
                sequences.append(current_sequence)

        # Kiểm tra các chuỗi liên tiếp theo đường chéo từ phải sang trái
        for start in range(2 * N - 1):
            count = 0
            current_sequence = []
            for row in range(N):
                col = start - row
                if 0 <= col < N:
                    if board[row][col] == player:
                        current_sequence.append((row, col))
                        count += 1
                    else:
                        if count > 1:
                            sequences.append(current_sequence)
                        count = 0
                        current_sequence = []
            if count > 1:
                sequences.append(current_sequence)

        return sequences

    def AI_move(self, boardState):
        self.goPoint = None
        score, move = self.alphaBeta(boardState, 0, -float("inf"), float("inf"), self.AI)
        print(score)
        print(max(self.scoreSet))
        return move
