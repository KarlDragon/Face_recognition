import tkinter as tk
from PIL import Image, ImageTk

class Client_UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Button Example")
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        Rx_position = screen_width * 2 // 3
        Ry_position = 0

        self.root_width = screen_width // 3
        self.root_height = screen_height // 3

        self.root.geometry(f"{self.root_width}x{self.root_height}+{Rx_position}+{Ry_position}")

        # Create a frame for the bottom row
        self.bottom_frame = tk.Frame(root, bg="white")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.bottom_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF66CC").pack(fill=tk.X)

        self.frame = tk.Frame(root, bg="#FFF0F5")
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Họ và tên:", height=2, font="large_font", bg="#FFF0F5").place(x=20, y=20)
        self.name_user = tk.Entry(self.frame, width=30)
        self.name_user.place(x=20, y=self.root_height*1//7)

        tk.Label(self.frame, text="Số báo danh:", height=2, font="large_font", bg="#FFF0F5").place(x=20, y=80)
        self.user_num = tk.Entry(self.frame, width=40)
        self.user_num.place(x=20, y=130)

        tk.Label(self.frame, text="Lớp:", height=2, font="large_font", bg="#FFF0F5").place(x=self.root_width*7//12, y=20)
        self.user_class = tk.Entry(self.frame)
        self.user_class.place(x=self.root_width*7//12, y=self.root_height*1//7)

        self.login_button = tk.Button(self.frame, text="Đăng nhập", width=75, height=2, command=self.on_button_click, bg="#FF69B4")
        self.login_button.place(x=40, y=self.root_height * 5 // 7 - 20)

    def on_button_click(self):
        name = self.name_user.get()
        num = self.user_num.get()
        class_ = self.user_class.get()

        for widget in self.frame.winfo_children():
            widget.destroy()

        time_left = "HH:MM:SS"
        tk.Label(self.frame, text=time_left, bg="pink", font=("Helvetica", 24)).place(x=450, y=10)

        tk.Label(self.frame, text=f"Tên: {name} Lớp: {class_} Số báo danh: {num}", bg="pink", font=("Helvetica", 15)).place(x=0, y=270)

if __name__ == "__main__":
    root = tk.Tk()
    app = Client_UI(root)
    root.mainloop()
