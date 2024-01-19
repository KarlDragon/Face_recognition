import tkinter as tk

class UI_UX:
    def __init__(self,root):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.iconbitmap(default=r"app_img\logo_app.ico")

