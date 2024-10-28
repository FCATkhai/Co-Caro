import tkinter as tk
from tkinter import font as tkfont
from MainGame import Game

class CaroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TRÍ TUỆ NHÂN TẠO NHÓM 12")

        self.root.geometry("800x800")  # Kích thước cửa sổ 800x800

        # Định nghĩa màu sắc
        self.bg_color = "#FFEBEE"  # Lavender blush background color
        self.text_color = "#0D1B2A"  # Rich black text color
        self.button_color = "#F8BBD0"  # Orchid pink button color
        self.button_text_color = "#0D1B2A"  # Rich black text color

        self.root.configure(bg=self.bg_color)  # Cấu hình màu nền của cửa sổ

        self.custom_font = tkfont.Font(family="Helvetica", size=17, weight="bold")  # Font-size tùy chỉnh

        # Tiêu đề
        self.label = tk.Label(root, text="CHÀO MỪNG ĐẾN CỜ CARO", font=("Helvetica", 24, "bold"), fg=self.text_color,
                              bg=self.bg_color)
        self.label.pack(pady=5)

        self.label = tk.Label(root, text="NHÓM 12", font=("Helvetica", 24, "bold"), fg=self.text_color, bg=self.bg_color)
        self.label.pack(pady=5)

        # Chế độ chơi (chỉ Người đấu AI)
        self.mode_label = tk.Label(root, text="Chế độ chơi: Người đấu AI", font=self.custom_font, fg=self.text_color,
                                   bg=self.bg_color)
        self.mode_label.pack(pady=10)

        # Nút bắt đầu và thoát
        self.start_button = tk.Button(root, text="Bắt đầu chơi", command=self.start_game, font=self.custom_font,
                                      fg=self.button_text_color, bg=self.button_color)
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(root, text="Thoát", command=self.exit_game, font=self.custom_font,
                                     fg=self.button_text_color, bg=self.button_color)
        self.exit_button.pack(pady=5)

    def start_game(self):
        size = 20  # Cố định kích thước bàn cờ là 20x20
        self.root.destroy()
        game = Game(size=size)
        game.mainloop()

    def exit_game(self):
        self.root.destroy()  # Đóng cửa sổ hiện tại và thoát ứng dụng


if __name__ == "__main__":
    root = tk.Tk()
    ui = CaroUI(root)
    root.mainloop()
