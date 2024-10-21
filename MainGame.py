import random
import tkinter as tk
from tkinter import messagebox
from Board import Board
from AI import AI

# --- Constants ---
DEFAULT_WIDTH = 800  # Chiều rộng mặc định của cửa sổ
DEFAULT_HEIGHT = 800  # Chiều cao mặc định của cửa sổ

BG_COLOR = "#FFEBEE"  # Lavender blush background color
LINE_COLOR = "#0D1B2A"  # Rich black line color
CIRC_COLOR = "#FF101F"  # Red circle (O) color
CROSS_COLOR = "#3E92CC"  # Celestial blue cross (X)
BUTTON_COLOR = "#F8BBD0"  # Orchid pink button color
BUTTON_TEXT_COLOR = "#0D1B2A"  # Rich black text color

WIN_LINE_COLOR = "#F5A742"  # Màu đường thắng (màu cam) F5A742
WIN_LINE_WIDTH = 10  # Độ dày của đường thắng
WIN_LINE_LENGTH = 1.2  # Tỷ lệ nhân để kéo dài đường kẻ


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
        self.canvas.bind("<Button-1>", self.handle_click)  # Ràng buộc sự kiện click chuột trái trên canvas

        # Reset button
        self.reset_button = tk.Button(self, text="Chơi lại", command=self.reset, font=("Helvetica", 16, "bold"),
                                      padx=20, pady=10, fg=BUTTON_TEXT_COLOR, bg=BUTTON_COLOR)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=20)
        # Back button
        self.back_button = tk.Button(self, text="Trở về", command=self.back, font=("Helvetica", 16, "bold"),
                                     padx=20, pady=10, fg=BUTTON_TEXT_COLOR, bg=BUTTON_COLOR)
        self.back_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Status label
        self.status_label = tk.Label(self, text="", font=("Helvetica", 20))
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
        if self.board.getPosition(row, col) == 1:
            start_desc = (col * self.sqsize + self.offset, row * self.sqsize + self.offset)
            end_desc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.sqsize - self.offset)
            self.canvas.create_line(*start_desc, *end_desc, fill=CROSS_COLOR, width=self.cross_width)

            start_asc = (col * self.sqsize + self.offset, row * self.sqsize + self.sqsize - self.offset)
            end_asc = (col * self.sqsize + self.sqsize - self.offset, row * self.sqsize + self.offset)
            self.canvas.create_line(*start_asc, *end_asc, fill=CROSS_COLOR, width=self.cross_width)
        elif self.board.getPosition(row, col) == 2:
            center = (col * self.sqsize + self.sqsize // 2, row * self.sqsize + self.sqsize // 2)
            self.canvas.create_oval(center[0] - self.radius, center[1] - self.radius,
                                    center[0] + self.radius, center[1] + self.radius,
                                    outline=CIRC_COLOR, width=self.circ_width)

    def make_move(self, row, col):
        if self.board.empty_sqr(row, col):
            self.board.setPosition(row, col, self.player)
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
            winner = "Người chơi 1" if result == 1 else "AI"
            self.draw_winning_line()
            self.status_label.config(text=f"{winner} đã thắng")  # Cập nhật status label
            messagebox.showinfo("Kết quả", f"{winner} đã thắng")  # Hiển thị hộp thoại thông báo
            self.running = False
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