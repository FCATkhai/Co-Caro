import numpy as np


class Board:
    def __init__(self, size):
        self.size = size  # Kích thước bàn cờ (NxN)
        self.squares = np.zeros((size, size), dtype=int)  # Khởi tạo bàn cờ với các ô vuông giá trị 0
        self.marked_sqrs = 0  # Số ô đã được đánh dấu
        self.max_item_win = 5  # Điều kiện thắng: 5 ô liên tiếp
        self.winning_line = None  # Để lưu đường thắng

    def getPosition(self, row, col):
        return self.squares[row][col]

    # Đánh dấu ô tại vị trí `row`, `col` với giá trị `player`
    def setPosition(self, row, col, player):
        self.squares[row][col] = player  # Đánh dấu ô với người chơi
        if player != 0:
            self.marked_sqrs += 1  # Tăng số ô đã đánh dấu
        else:
            self.marked_sqrs -= 1

    # Kiểm tra trạng thái kết thúc (thắng/thua) sau khi đánh một nước
    # tra ve nguoi chien thang neu ket thuc, nguoc lai tra ve 0
    def final_state(self, marked_row, marked_col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Các hướng kiểm tra (dọc, ngang, chéo phải, chéo trái)
        player = self.squares[marked_row][marked_col]  # Người chơi hiện tại

        for dr, dc in directions:  # Duyệt qua mỗi hướng để kiểm tra thắng
            count = 0  # Khởi tạo biến đếm số ô liên tiếp
            start = None
            for delta in range(-self.max_item_win + 1,
                               self.max_item_win):  # Duyệt qua khoảng giá trị từ -max_item_win + 1 đến max_item_win
                r = marked_row + delta * dr  # Tính toán vị trí dọc
                c = marked_col + delta * dc  # Tính toán vị trí ngang
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.squares[r][c] == player:
                        if count == 0:
                            start = (r, c)
                        count += 1
                        if count == self.max_item_win:
                            self.winning_line = (start, (r, c))
                            return player
                    else:
                        count = 0
                        start = None
                else:
                    count = 0
                    start = None
        return 0

    # Đánh dấu ô tại vị trí `row`, `col` với giá trị `player`
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player  # Đánh dấu ô với người chơi
        if player != 0:
            self.marked_sqrs += 1  # Tăng số ô đã đánh dấu
        else:
            self.marked_sqrs -= 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0  # Tăng số ô đã đánh dấu

    def get_empty_sqrs(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if
                self.empty_sqr(r, c)]  # Lấy danh sách các ô trống

    def is_full(self):
        return self.marked_sqrs == self.size * self.size  # Kiểm tra bàn cờ có đầy không
