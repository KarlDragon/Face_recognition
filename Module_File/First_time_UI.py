import tkinter as tk
import sys
import os
class UI_UX:
    def __init__(self,root):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        if getattr(sys, 'frozen', False):
            # Ứng dụng đang chạy trong môi trường được đóng gói (executable)
            self.current_directory = os.path.dirname(sys.executable)
        else:
            # Ứng dụng đang chạy trong môi trường không được đóng gói (script)
            self.current_directory = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(self.current_directory, 'app_img', 'logo_app.ico')
        self.root.iconbitmap(default=logo_path)
        
class First_time_UI(UI_UX):
    def __init__(self,root):
        self.mode=None
        super().__init__(root)

    #UI for the first
    def user_mode_button(self,mode):
        if mode=="Sv":
            self.mode_button_sv.config(relief=tk.SUNKEN)
            self.mode_button_cl.config(relief=tk.RAISED)
            self.mode=mode
        
        if mode=="Cl":
            self.mode_button_cl.config(relief=tk.SUNKEN)
            self.mode_button_sv.config(relief=tk.RAISED)
            self.mode=mode
        
    def user_infor(self,mode,path,IP,port,amount):
        with open('information.txt','w') as f:
            f.writelines(mode)
            f.writelines("\n")
            f.writelines(path.get())
            f.writelines("\n")
            f.writelines(IP.get())
            f.writelines("\n")
            f.writelines(port.get())
            f.writelines("\n")
            if mode=="Sv":
                f.writelines(amount.get())
        self.root.destroy()
        
    def FT_UI(self):
        self.Sx_position = self.screen_width//2 - 300
        self.Sy_position = self.screen_height//2-200

        self.root_width = 600 
        self.root_height = 500
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Sx_position}+{self.Sy_position}")

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill=tk.BOTH,expand=True)
        self.inf_frame = tk.Frame(self.frame, bg="white")
        self.inf_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.inf_frame, text="Nhập thông tin", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF69B4").pack(fill=tk.X)

        self.mode_frame = tk.Frame(self.frame, bg="white")
        self.mode_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.mode_frame, text="Bạn là: ", height=2,width=20, fg="black", font=("Helvetica", 15, "bold"), bg="white").pack(side=tk.LEFT,pady=10)
        
        self.mode_button_sv = tk.Button(self.mode_frame, text="Máy chủ", width=20, height=3,command=lambda: self.user_mode_button("Sv"), bg="#FF99CC")
        self.mode_button_sv.pack(side=tk.LEFT,pady=10)
        
        self.mode_button_cl = tk.Button(self.mode_frame, text="Máy khách", width=20, height=3,command=lambda: self.user_mode_button("Cl"), bg="#FF99CC")
        self.mode_button_cl.pack(side=tk.LEFT,pady=10)

        self.path_frame = tk.Frame(self.frame, bg="white")
        self.path_frame.pack(side=tk.TOP, fill=tk.X,pady=10)
        
        tk.Label(self.path_frame, text="                    Nhập đường dẫn: ", height=2, font="large_font", bg="white").pack(side=tk.LEFT)
        
        self.path = tk.Entry(self.path_frame, width=40)
        self.path.config(highlightthickness=1, highlightbackground="black")
        self.path.pack(side=tk.LEFT)

        self.IP_frame = tk.Frame(self.frame, bg="white")
        self.IP_frame.pack(side=tk.TOP, fill=tk.X,pady=10)
        
        tk.Label(self.IP_frame, text="                    Nhập IP: ", height=2, font="large_font", bg="white").pack(side=tk.LEFT)
        
        self.IP = tk.Entry(self.IP_frame, width=51)
        self.IP.config(highlightthickness=1, highlightbackground="black")
        self.IP.pack(side=tk.LEFT)

        self.port_frame = tk.Frame(self.frame, bg="white")
        self.port_frame.pack(side=tk.TOP, fill=tk.X,pady=10)
        
        tk.Label(self.port_frame, text="                    Nhập cổng: ", height=2, font="large_font", bg="white").pack(side=tk.LEFT)
        
        self.port = tk.Entry(self.port_frame, width=48)
        self.port.config(highlightthickness=1, highlightbackground="black")
        self.port.pack(side=tk.LEFT)

        self.notice_frame = tk.Frame(self.frame, bg="white")
        self.notice_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.notice_frame, text="                    (*Nếu bạn là máy chủ) ", height=1, font="small_font", bg="white", fg="red").pack(side=tk.LEFT)
        
        self.amount_frame = tk.Frame(self.frame, bg="white")
        self.amount_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.amount_frame, text="                    Nhập số lượng máy khách: ", height=2, font="large_font", bg="white").pack(side=tk.LEFT)
        
        self.amount = tk.Entry(self.amount_frame, width=30)
        self.amount.config(highlightthickness=1, highlightbackground="black")
        self.amount.pack(side=tk.LEFT)

        self.mode_button = tk.Button(self.frame, text="Hoàn tất", width=20, height=3,command=lambda: self.user_infor(self.mode,self.path,self.IP,self.port,self.amount), bg="#FF69B4")
        self.mode_button.pack(side=tk.TOP,pady=10)


def run_gui_ft():
    root = tk.Tk()
    app = First_time_UI(root)
    app.FT_UI()
    root.mainloop()
