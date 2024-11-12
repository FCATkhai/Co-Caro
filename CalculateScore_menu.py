import tkinter as tk
from tkinter import messagebox, font
from Board import Board
from CalculateScore import evaluateBoard

# --- Constants ---
DEFAULT_BOARD_WIDTH = 400  # Chiều rộng mặc định của bàn cờ
DEFAULT_BOARD_HEIGHT = 400  # Chiều cao mặc định của bàn cờ
DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 600

BG_COLOR = "#FFEBEE"  # Lavender blush background color
LINE_COLOR = "#0D1B2A"  # Rich black line color
CIRC_COLOR = "#FF101F"  # Red circle (O) color
CROSS_COLOR = "#3E92CC"  # Celestial blue cross (X)
BUTTON_COLOR = "#F8BBD0"  # Orchid pink button color
BUTTON_TEXT_COLOR = "#0D1B2A"  # Rich black text color

WIN_LINE_COLOR = "#F5A742"  # Màu đường thắng (màu cam) F5A742
WIN_LINE_WIDTH = 10  # Độ dày của đường thắng
WIN_LINE_LENGTH = 1.2  # Tỷ lệ nhân để kéo dài đường kẻ


class CalculateScore_menu(tk.Tk):
    def __init__(self, size=5):
        super().__init__()
        self.title("TRÍ TUỆ NHÂN TẠO NHÓM 12")  # Tiêu đề cửa sổ
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT + 100}+300+50")  # Kích thước cửa sổ
        self.canvas = tk.Canvas(self, width=DEFAULT_BOARD_WIDTH, height=DEFAULT_BOARD_HEIGHT, bg=BG_COLOR)  # Tạo canvas
        self.canvas.pack(side=tk.TOP, fill=tk.NONE)

        self.size = size  # Kích thước bàn cờ
        self.sqsize = DEFAULT_WIDTH // self.size  # Kích thước mỗi ô vuông trên bảng
        self.radius = self.sqsize // 4  # Bán kính của dấu tròn (O)
        self.offset = self.sqsize // 4  # Khoảng cách bù trừ cho việc vẽ dấu
        self.line_width = self.offset // 4  # Độ dày của các đường kẻ
        self.circ_width = self.offset // 2  # Độ dày của đường kẻ dấu tròn (O)
        self.cross_width = self.offset // 2  # Độ dày của đường kẻ dấu chéo (X)

        self.board = Board(self.size)  # Tạo bảng chơi với kích thước được chỉ định

        self.player = 1  # Người chơi bắt đầu
        self.running = True  # Trạng thái trò chơi đang chạy
        self.show_lines()  # Vẽ lưới bàn cờ
        self.canvas.bind("<Button-1>", self.handle_click)  # Ràng buộc sự kiện click chuột trái trên canvas

        # Status label
        self.status_label = tk.Label(self, text="", font=("Helvetica", 20))
        self.status_label.pack(pady=20)

        # EvalBoard button
        self.eval_button = tk.Button(self, text="Tính điểm", command=self.evalBoard, font=("Helvetica", 16, "bold"),
                                     padx=20, pady=10, fg=BUTTON_TEXT_COLOR, bg=BUTTON_COLOR)
        self.eval_button.pack(padx=20, pady=10)

        # Reset button
        self.reset_button = tk.Button(self, text="Reset", command=self.reset, font=("Helvetica", 16, "bold"),
                                      padx=20, pady=10, fg=BUTTON_TEXT_COLOR, bg=BUTTON_COLOR)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Back button
        self.back_button = tk.Button(self, text="Trở về", command=self.back, font=("Helvetica", 16, "bold"),
                                     padx=20, pady=10, fg=BUTTON_TEXT_COLOR, bg=BUTTON_COLOR)
        self.back_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Hiển thị các đường kẻ trên bảng
    def show_lines(self):
        self.canvas.delete("all")  # Xóa tất cả các phần tử trên canvas
        for col in range(1, self.size):
            x = col * self.sqsize
            self.canvas.create_line(x, 0, x, DEFAULT_HEIGHT - 100, fill=LINE_COLOR, width=self.line_width)
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
        player_turn = "X" if self.player == 1 else "O"
        self.status_label.config(text=f"Lượt của {player_turn}")  # Cập nhật status label

    def is_over(self, row, col):
        result = self.board.final_state(row, col)
        if result != 0:
            winner = "X" if result == 1 else "O"
            self.draw_winning_line()
            self.status_label.config(text=f"{winner} đã thắng")  # Cập nhật status label
            custom_message_box("Kết quả", f"{winner} đã thắng")
            # messagebox.showinfo("Kết quả", f"{winner} đã thắng")  # Hiển thị hộp thoại thông báo
            self.running = False
            return True
        elif self.board.is_full():  # Hòa
            self.status_label.config(text="Hòa")  # Cập nhật status label
            messagebox.showinfo("Kết quả", "Hòa")
            self.running = False  # Dừng trò chơi
            return True
        return False

    def handle_click(self, event):
        if not self.running:  # Nếu trò chơi không chạy
            return

        col = event.x // self.sqsize  # Tính toán cột
        row = event.y // self.sqsize  # Tính toán hàng

        if self.board.empty_sqr(row, col):  # Nếu ô vuông trống
            if self.make_move(row, col):  # Thực hiện nước đi
                self.canvas.update()  # Cập nhật canvas ngay lập tức
                self.is_over(row, col)  # Nếu trò chơi chưa kết thúc
        else:
            self.status_label.config(text="Ô này đã được đánh!")  # Hiển thị thông báo ô đã được đánh
            self.update()  # Cập nhật giao diện ngay lập tức

    def evalBoard(self):

        score = evaluateBoard(self.board, 2)
        self.option_add('*Dialog.msg.font', 'Helvetica 18')
        custom_message_box("Điểm", f"Điểm của trạng thái bàn cờ là {score:.2f}")
        self.option_clear()

    def reset(self):
        self.running = True
        self.board = Board(self.size)  # Khởi tạo lại bàn cờ
        self.player = 1  # Đặt lại người chơi về người chơi 1
        self.show_lines()  # Vẽ lại lưới
        self.status_label.config(text="Bắt đầu trò chơi mới")  # Cập nhật status label
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


def custom_message_box(title, message, font_family="Helvetica", font_size=25):
    # Create a Toplevel window for the custom message box
    box = tk.Toplevel()
    box.title(title)
    box.geometry("400x250")
    box.grab_set()  # Grab focus to this window

    # Configure custom font
    custom_font = font.Font(family=font_family, size=font_size)

    # Add message label
    message_label = tk.Label(box, text=message, font=custom_font, wraplength=280)
    message_label.pack(pady=20)

    # Add OK button
    ok_button = tk.Button(box, text="OK", command=box.destroy)
    ok_button.pack(pady=10)

if __name__ == '__main__':
    game = CalculateScore_menu()  # Tạo đối tượng game
    game.mainloop()  # Bắt đầu vòng lặp chính của giao diện
