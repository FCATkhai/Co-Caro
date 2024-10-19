import copy
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time
from functools import lru_cache

# --- Constants ---
DEFAULT_WIDTH = 800  # Chiều rộng mặc định của cửa sổ
DEFAULT_HEIGHT = 800  # Chiều cao mặc định của cửa sổ

BG_COLOR = "#F5F5DC"  # Beige background color
LINE_COLOR = "#8B4513"  # Dark Brown line color
CIRC_COLOR = "#006400"  # Dark Green circle (O) color
CROSS_COLOR = "#8B0000"  # Dark Red cross (X) color

WIN_LINE_COLOR = "#F5A742"  # Màu đường thắng (màu cam)
WIN_LINE_WIDTH = 15  # Độ dày của đường thắng
WIN_LINE_LENGTH = 1.2  # Tỷ lệ nhân để kéo dài đường kẻ


class Board:
    def __init__(self, size):
        self.size = size  # Kích thước bàn cờ (NxN)
        self.squares = np.zeros((size, size), dtype=int)  # Khởi tạo bàn cờ với các ô vuông giá trị 0
        self.marked_sqrs = 0  # Số ô đã được đánh dấu
        self.max_item_win = 3 if size == 5 else 5  # Điều kiện thắng (3 liên tiếp cho 5x5, 5 liên tiếp cho các kích thước khác)
        self.winning_line = None  # Để lưu đường thắng

    # Kiểm tra trạng thái kết thúc (thắng/thua) sau khi đánh một nước
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


class AI:
    def __init__(self, player=2):  # Số đại diện cho AI (thường là 2)
        self.player = player
        self.opponent = 3 - player  # Số đại diện cho đối thủ (thường là 1)


#--------------------------------------------------------------------------

    
    def AI_move_2(self, board):  # AI
        max_val = float('-inf')  # khởi tạo mặc định là âm vô cùng
        final_row = -1
        final_col = -1 
        
        # Duyệt các điểm chưa đánh trong bảng để tìm ra điểm tốt nhất (mảng 1 chiều)
        for row in range(board.size):  # board.size là kích thước bàn cờ (mặc định là 15 ô)
            for col in range(board.size):
                if board.squares[row][col] == 0: # ô được đánh dấu mang giá trị 0 (rỗng) thì đánh X
                    temp_board = copy.deepcopy(board)
                    temp_board.mark_sqr(row, col, self.player)
                    
                    mark = self.getMark(row, col, temp_board)
                    
                    temp_board.mark_sqr(row, col, 0)  # trả giá trị về rỗng
                    if mark > max_val:  # lưu điểm tốt nhất tìm được
                        final_col = col
                        final_row = row
                        max_val = mark
        
        return (final_row, final_col)



    def getMark(self, row, col, board):
            # Trọng số đánh giá
        tancong = [0, 2, 4, 20, 100, 105, 110, 115, 120, 130]
        phongthu = [0, 1, 3, 15, 55, 56, 57, 58, 60, 62]
        
        result = tancong[self.getNgang(row, col, board, self.player)] + tancong[self.getDoc(row, col, board, self.player)] + \
                tancong[self.getCheo1(row, col, board, self.player)] + tancong[self.getCheo2(row, col, board, self.player)]
        
        result += phongthu[self.getNgang(row, col, board, self.opponent)] + phongthu[self.getDoc(row, col, board, self.opponent)] + \
                phongthu[self.getCheo1(row, col, board, self.opponent)] + phongthu[self.getCheo2(row, col, board, self.opponent)]
        
        return result

    # Đếm trên hàng ngang
    def getNgang(self, row, col, board, player):
        count = 0  # đếm giá trị giống player
        block = 0  # Đếm số lần bị chặn
        
        # duyệt trước
        for i in range(col - 1, 0, -1):
            if board.squares[row][i] == player:
                count += 1  # nếu board.squares tại vị trí giống giá trị ở điểm hiện tại player thì +1 count
            else:
                if board.squares[row][i] != 0:  # nếu board.squares tại vị trí không bằng rỗng thì bị chặn -> +1 block
                    block += 1
                break
        
        # duyệt sau
        for i in range(col + 1, board.size):
            if board.squares[row][i] == player:
                count += 1
            else:
                if board.squares[row][i] != 0:
                    block += 1
                break
        
        if block == 2:
            return 0  # Bị chặn cả 2 đầu
        if (col == 0 or col == board.size - 1) and count < 4:
            block += 1  # Điểm sát cạnh +1 block
        if count <= block:
            return 0  # Bị chặn nhiều hơn
        elif count - block >= 3:
            return count + block  # Xảy ra khi x thắng hoặc o sắp thắng
        else:
            return count - block  # < 3

    # Đếm trên hàng dọc
    def getDoc(self, row, col, board, player):
        count = 0
        block = 0
        
        for i in range(row - 1, 0, -1):
            if board.squares[i][col] == player:
                count += 1
            else:
                if board.squares[i][col] != 0:
                    block += 1
                break
        
        for i in range(row + 1, board.size):
            if board.squares[i][col] == player:
                count += 1
            else:
                if board.squares[i][col] != 0:
                    block += 1
                break
        
        if block == 2:
            return 0
        if (row == 0 or row == board.size - 1) and count < 4:
            block += 1
        if count <= block:
            return 0
        elif count - block >= 3:
            return count + block
        else:
            return count - block

    # Đếm trên đường chéo / (từ dưới lên)
    def getCheo1(self, row, col, board, player):
        count = 0
        block = 0
        
        for i in range(1, min(board.size - col, row + 1)):
            if board.squares[row - i][col + i] == player:
                count += 1
            else:
                if board.squares[row - i][col + i] != 0:
                    block += 1
                break
        
        for i in range(1, min(col + 1, board.size - row)):
            if board.squares[row + i][col - i] == player:
                count += 1
            else:
                if board.squares[row + i][col - i] != 0:
                    block += 1
                break
        
        if block == 2:
            return 0
        if (col == 0 or col == board.size - 1 or row == 0 or row == board.size - 1) and count < 4:
            block += 1
        if count <= block:
            return 0
        elif count - block >= 3:
            return count + block
        else:
            return count - block

    # Đếm trên đường chéo \ (từ dưới lên)
    def getCheo2(self, row, col, board, player):
        count = 0
        block = 0
        
        for i in range(1, min(col + 1, row + 1)):
            if board.squares[row - i][col - i] == player:
                count += 1
            else:
                if board.squares[row - i][col - i] != 0:
                    block += 1
                break
        
        for i in range(1, min(board.size - col, board.size - row)):
            if board.squares[row + i][col + i] == player:
                count += 1
            else:
                if board.squares[row + i][col + i] != 0:
                    block += 1
                break
        
        if block == 2:
            return 0
        if (col == 0 or col == board.size - 1 or row == 0 or row == board.size - 1) and count < 4:
            block += 1
        if count <= block:
            return 0
        elif count - block >= 3:
            return count + block
        else:
            return count - block
        
        
        
    
# -----------------------------------------------------


class Game(tk.Tk):
    def __init__(self, size=16, gamemode='ai'):
        super().__init__()
        self.title("010100085803-TRÍ TUỆ NHÂN TẠO-NHÓM 5")  # Tiêu đề cửa sổ
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT + 100}")  # Kích thước cửa sổ
        self.canvas = tk.Canvas(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, bg=BG_COLOR)  # Tạo canvas
        self.canvas.pack()

        self.size = size  # Kích thước bàn cờ
        self.sqsize = DEFAULT_WIDTH // self.size  # Kích thước mỗi ô vuông trên bảng
        self.radius = self.sqsize // 4  # Bán kính của dấu tròn (O)
        self.offset = self.sqsize // 4  # Khoảng cách bù trừ cho việc vẽ dấu
        self.line_width = self.offset // 2  # Độ dày của các đường kẻ
        self.circ_width = self.offset // 2  # Độ dày của đường kẻ dấu tròn (O)
        self.cross_width = self.offset // 2  # Độ dày của đường kẻ dấu chéo (X)

        self.board = Board(self.size)  # Tạo bảng chơi với kích thước được chỉ định
        self.ai = AI()  # Tạo đối tượng AI
        self.player = 1  # Người chơi bắt đầu
        self.gamemode = gamemode  # Chế độ chơi (Player vs Player or Player vs A.I)
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
            if self.gamemode == 'pvp' or self.player == 1:
                if self.make_move(row, col):  # Thực hiện nước đi
                    self.canvas.update()  # Cập nhật canvas ngay lập tức
                    if not self.is_over(row, col):  # Nếu trò chơi chưa kết thúc
                        if self.gamemode == 'ai' and self.running:
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
            move = self.ai.AI_move_2(self.board)  # AI tính toán nước đi
            if move:
                self.after(0, lambda: self.make_ai_move(move))
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

        # Nếu đang ở chế độ AI và AI đi trước (người chơi 2), thực hiện nước đi của AI
        if self.gamemode == 'ai' and self.player == 2:
            self.after(100, self.ai_turn)

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