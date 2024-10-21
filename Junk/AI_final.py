import copy
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox


# --- Constants ---
DEFAULT_WIDTH = 800  # Chiều rộng mặc định của cửa sổ
DEFAULT_HEIGHT = 800  # Chiều cao mặc định của cửa sổ

BG_COLOR = "#FFEBEE"  # Lavender blush background color
LINE_COLOR = "#0D1B2A"  # Rich black line color
CIRC_COLOR = "#FF101F"  # Red circle (O) color
CROSS_COLOR = "#3E92CC"  # Celestial blue cross (X)

WIN_LINE_COLOR = "#F5A742"  # Màu đường thắng (màu cam) F5A742
WIN_LINE_WIDTH = 10  # Độ dày của đường thắng
WIN_LINE_LENGTH = 1.2  # Tỷ lệ nhân để kéo dài đường kẻ


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
            for delta in range(-self.max_item_win + 1, self.max_item_win):  # Duyệt qua khoảng giá trị từ -max_item_win + 1 đến max_item_win
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


class AI:
    def __init__(self, player=2):  # Số đại diện cho AI (thường là 2)
        self.AI = player
        self.opponent = 3 - player  # Số đại diện cho đối thủ (thường là 1)
        self.eBoard = EvalBoard()
        self.AScore = [0, 4, 27, 256, 1458]
        self.DScore = [0, 2, 9, 99, 769]
        self.maxDepth = 4
        self.maxMove = 4
        self.goPoint = None

    def evalChessBoard(self, player, boardState, eBoard):
        eBoard.resetBoard()
        # Duyet theo hang (Scan by row)
        for row in range(eBoard.size):
            for col in range(eBoard.size - 4):
                eAI = 0
                eHuman = 0
                for i in range(5):
                    if boardState.getPosition(row, col + i) == self.opponent:  # neu quan do la cua human 
                        eHuman += 1
                    if boardState.getPosition(row, col + i) == self.AI:  # neu quan do la cua pc 
                        eAI += 1
                # Trong vong 5 o khong co quan dich 
                if eHuman * eAI == 0 and eHuman != eAI:
                    for i in range(5):
                        if boardState.getPosition(row, col + i) == 0:  # neu o chua danh 
                            if eHuman == 0:  # ePC khac 0 
                                if player == 1:
                                    eBoard.EBoard[row][col + i] += self.DScore[eAI]  # cho diem phong ngu
                                else:
                                    eBoard.EBoard[row][col + i] += self.AScore[eAI]  # cho diem tan cong 
                            if eAI == 0:  # eHuman khac 0 
                                if player == 2:
                                    eBoard.EBoard[row][col + i] += self.DScore[eHuman]  # cho diem phong ngu
                                else:
                                    eBoard.EBoard[row][col + i] += self.AScore[eHuman]  # cho diem tan cong
                            if eHuman == 4 or eAI == 4:
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

        # Duyet theo duong cheo xuong
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

        # Duyet theo duong cheo len 
        for row in range(4, eBoard.size):
            for col in range(eBoard.size - 4):
                eAI = 0  # so quan PC 
                eHuman = 0  # so quan Human
                for i in range(5):
                    if boardState.getPosition(row - i, col + i) == 1:  # neu la human
                        eHuman += 1  # tang so quan human
                    if boardState.getPosition(row - i, col + i) == 2:  # neu la PC 
                        eAI += 1  # tang so quan PC
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

        self.evalChessBoard(2, boardState, self.eBoard)
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
                return v
            alpha = max(alpha, v)

        return v

    def minValue(self, boardState, alpha, beta, depth):
        self.eBoard.maxPos()
        value = self.eBoard.evaluationBoard
        if depth >= self.maxDepth:
            return value

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
                return v
            beta = min(beta, v)

        return v

    def AI_move(self, boardState):
        self.goPoint = None
        self.alphaBeta(boardState, 0, 1, 0, self.AI)
        return self.goPoint


class Game(tk.Tk):
    def __init__(self, size=20):
        super().__init__()
        self.title("TRÍ TUỆ NHÂN TẠO NHÓM 12")  # Tiêu đề cửa sổ
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT + 100}")  # Kích thước cửa sổ
        self.canvas = tk.Canvas(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, bg=BG_COLOR)  # Tạo canvas
        self.canvas.pack()

        self.size = size  # Kích thước bàn cờ
        self.sqsize = DEFAULT_WIDTH // self.size  # Kích thước mỗi ô vuông trên bảng
        self.radius = self.sqsize // 4  # Bán kính của dấu tròn (O)
        self.offset = self.sqsize // 4  # Khoảng cách bù trừ cho việc vẽ dấu
        self.line_width = self.offset // 4  # Độ dày của các đường kẻ
        self.circ_width = self.offset // 2  # Độ dày của đường kẻ dấu tròn (O)
        self.cross_width = self.offset // 2  # Độ dày của đường kẻ dấu chéo (X)

        self.board = Board(self.size)  # Tạo bảng chơi với kích thước được chỉ định
        self.ai = AI()  # Tạo đối tượng AI
        self.player = 1  # Người chơi bắt đầu
        self.running = True  # Trạng thái trò chơi đang chạy
        self.ai_thinking = False  # Trạng thái AI đang suy nghĩ
        self.show_lines()  # Vẽ lưới bàn cờ
        self.canvas.bind("<Button-1>", self.handle_click)  # Ràng buộc sự kiện click chuột trên canvas

        # Reset button
        self.reset_button = tk.Button(self, text="Chơi lại", command=self.reset, font=("Times New Roman", 16, "bold"),
                                      padx=20, pady=10)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=20)
        # Back button
        self.back_button = tk.Button(self, text="Trở về", command=self.back, font=("Times New Roman", 16, "bold"),
                                     padx=20, pady=10)
        self.back_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Status label
        self.status_label = tk.Label(self, text="", font=("Times New Roman", 20))
        self.status_label.pack(pady=10)

    # Hiển thị các đường kẻ trên bảng
    def show_lines(self):
        self.canvas.delete("all")  # Xóa tất cả các phần tử trên canvas
        for col in range(1, self.size):
            x = col * self.sqsize
            self.canvas.create_line(x, 0, x, DEFAULT_HEIGHT, fill=LINE_COLOR, width=self.line_width)
        for row in range(1, self.size):
            y = row * self.sqsize
            self.canvas.create_line(0, y, DEFAULT_WIDTH, y, fill=LINE_COLOR, width=self.line_width)

    # Vẽ ký hiệu X hoặc O lên bàn cờ
    def draw_fig(self, row, col):
        if self.board.squares[row][col] == 1:
            start_desc = (col * self.sqsize + self.offset, row * self.sqsize + self.offset)
            end_desc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.sqsize - self.offset)
            self.canvas.create_line(*start_desc, *end_desc, fill=CROSS_COLOR, width=self.cross_width)

            start_asc = (col * self.sqsize + self.offset, row * self.sqsize + self.sqsize - self.offset)
            end_asc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.offset)
            self.canvas.create_line(*start_asc, *end_asc, fill=CROSS_COLOR, width=self.cross_width)
        elif self.board.squares[row][col] == 2:
            center = (col * self.sqsize + self.sqsize // 2, row * self.sqsize + self.sqsize // 2)
            self.canvas.create_oval(center[0] - self.radius, center[1] - self.radius,
                                    center[0] + self.radius, center[1] + self.radius,
                                    outline=CIRC_COLOR, width=self.circ_width)

    def make_move(self, row, col):
        if self.board.empty_sqr(row, col):
            self.board.mark_sqr(row, col, self.player)
            self.draw_fig(row, col)
            self.canvas.update()  # Cập nhật canvas ngay lập tức
            self.next_turn()
            return True
        return False

    def next_turn(self):
        self.player = self.player % 2 + 1  # Chuyển lượt người chơi
        self.status_label.config(text=f"Lượt của Người chơi {self.player}")  # Cập nhật status label

    # Hàm kẻ đường win
    def draw_winning_line(self):
        if self.board.winning_line:
            start, end = self.board.winning_line
            start_x = start[1] * self.sqsize + self.sqsize // 2
            start_y = start[0] * self.sqsize + self.sqsize // 2
            end_x = end[1] * self.sqsize + self.sqsize // 2
            end_y = end[0] * self.sqsize + self.sqsize // 2
            # Tính toán độ dài của đường kẻ chiến thắng
            delta_x = end_x - start_x
            delta_y = end_y - start_y
            start_x -= delta_x * (WIN_LINE_LENGTH - 1) / 2
            start_y -= delta_y * (WIN_LINE_LENGTH - 1) / 2
            end_x += delta_x * (WIN_LINE_LENGTH - 1) / 2
            end_y += delta_y * (WIN_LINE_LENGTH - 1) / 2
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=WIN_LINE_COLOR, width=WIN_LINE_WIDTH)

    def is_over(self, row, col):
        result = self.board.final_state(row, col)
        if result != 0:
            winner = "Người chơi 1" if result == 1 else "Người chơi 2"
            self.draw_winning_line()
            messagebox.showinfo("Kết quả", f"{winner} đã thắng")  # Hiển thị hộp thoại thông báo
            self.running = False
            self.status_label.config(text=f"{winner} đã thắng")  # Cập nhật status label
            return True
        elif self.board.is_full():  # Hòa
            messagebox.showinfo("Kết quả", "Hòa")
            self.running = False  # Dừng trò chơi
            self.status_label.config(text="Hòa")  # Cập nhật status label
            return True
        return False

    def handle_click(self, event):
        if not self.running or self.ai_thinking:  # Nếu trò chơi không chạy hoặc AI đang suy nghĩ
            return

        col = event.x // self.sqsize  # Tính toán cột
        row = event.y // self.sqsize  # Tính toán hàng

        if self.board.empty_sqr(row, col):  # Nếu ô vuông trống
            if self.player == 1:
                if self.make_move(row, col):  # Thực hiện nước đi
                    self.canvas.update()  # Cập nhật canvas ngay lập tức
                    if not self.is_over(row, col):  # Nếu trò chơi chưa kết thúc
                        if self.running:
                            self.status_label.config(text="AI đang suy nghĩ...")
                            self.update()  # Cập nhật giao diện ngay lập tức
                            self.after(100, self.ai_turn)  # AI thực hiện nước đi
        else:
            self.status_label.config(text="Ô này đã được đánh!")  # Hiển thị thông báo ô đã được đánh
            self.update()  # Cập nhật giao diện ngay lập tức
    def ai_turn(self):
        self.ai_thinking = True
        self.status_label.config(text="AI đang suy nghĩ...")
        self.update()  # Cập nhật giao diện ngay lập tức

        def ai_move():
            move = self.ai.AI_move(self.board)  # AI tính toán nước đi
            if move:
                self.after(0, self.make_ai_move(move))
            else:
                self.after(0, self.handle_ai_no_move)

        self.after(100, ai_move)  # Sử dụng after thay vì threading

    def make_ai_move(self, move):
        row, col = move
        if self.make_move(row, col):  # AI thực hiện nước đi
            self.canvas.update()  # Cập nhật canvas ngay lập tức
            if not self.is_over(row, col):  # Nếu trò chơi chưa kết thúc
                self.status_label.config(text="Lượt của bạn")
            self.ai_thinking = False
        else:
            print("AI không thể thực hiện nước đi này!")
            self.handle_ai_no_move()

    def handle_ai_no_move(self):
        print("AI không tìm được nước đi hợp lệ!")
        empty_sqrs = self.board.get_empty_sqrs()
        if empty_sqrs:
            move = random.choice(empty_sqrs)  # Chọn ngẫu nhiên nước đi
            self.make_ai_move(move)
        else:
            self.status_label.config(text="Hòa - Không còn nước đi!")  # Hiển thị thông báo hòa
            self.running = False
        self.ai_thinking = False

    def reset(self):
        self.board = Board(self.size)  # Khởi tạo lại bàn cờ
        self.running = True  # Bắt đầu trò chơi mới
        self.ai_thinking = False
        self.player = 1  # Đặt lại người chơi về người chơi 1
        self.show_lines()  # Vẽ lại lưới
        self.status_label.config(text="Bắt đầu trò chơi mới. Lượt của Người chơi 1")  # Cập nhật status label
        self.canvas.delete("all")  # Xóa tất cả các phần tử trên canvas
        self.show_lines()  # Vẽ lại lưới
        self.board.winning_line = None  # Đặt lại đường thắng

        self.update()  # Cập nhật giao diện

    def back(self):
        self.destroy()  # Đóng cửa sổ hiện tại
        import caro_menu  # Quay lại form menu
        root = tk.Tk()  # Tạo cửa sổ mới
        caro_menu.CaroUI(root)  # Khởi tạo giao diện menu
        root.mainloop()  # Chạy vòng lặp chính của giao diện

    def update(self):
        self.canvas.update()  # Cập nhật canvas
        self.update_idletasks()  # Cập nhật các tác vụ nền


if __name__ == '__main__':
    game = Game()  # Tạo đối tượng game
    game.mainloop()  # Bắt đầu vòng lặp chính của giao diện

