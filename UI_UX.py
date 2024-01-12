import tkinter as tk
from PIL import Image, ImageTk

class UI_UX:
    def __init__(self, root, mode,cam_num,folder_num):
        self.root = root
        self.root.title("Huỳnh Gia Thiên")
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        check=True
        if check:
            self.First_time_UI(screen_width,screen_height)
        if not check:
            if mode=="Cl":
                self.Client_UI(screen_width,screen_height)

            if mode=="Sv":
                self.Sever_UI(screen_width,screen_height,cam_num, folder_num)
                
    def Client_main(self):
        name = self.name_user.get()
        num = self.user_num.get()
        class_ = self.user_class.get()

        for widget in self.frame.winfo_children():
            widget.destroy()

        time_left = "HH:MM:SS"
        tk.Label(self.frame, text=time_left, bg="pink", font=("Helvetica", 24)).place(x=450, y=10)

        tk.Label(self.frame, text=f"Tên: {name} Lớp: {class_} Số báo danh: {num}", bg="pink", font=("Helvetica", 15)).place(x=0, y=270)

    def Client_UI(self,screen_width,screen_height):
        self.Cx_position = screen_width * 2 // 3
        self.Cy_position = 0

        self.root_width = screen_width // 3
        self.root_height = screen_height // 3
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Cx_position}+{self.Cy_position}")

        self.bottom_frame = tk.Frame(self.root, bg="white")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.bottom_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF66CC").pack(fill=tk.X)

        self.frame = tk.Frame(self.root, bg="#FFF0F5")
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

        self.login_button = tk.Button(self.frame, text="Đăng nhập", width=75, height=2, command=self.Client_main, bg="#FF69B4")
        self.login_button.place(x=40, y=self.root_height * 5 // 7 - 20)
        
    def show_cam(self):
        pass

    def show_folder(self, search, folder_list, canvas):
        index = int(search.get()) - 1

        # Prompt the user to select a folder
        selected_folder = filedialog.askdirectory(title="Select a Folder")
        if not selected_folder:  # User canceled the operation
            return

        # Clear the previous content of the canvas
        for widget in canvas.winfo_children():
            widget.destroy()

        # Display the contents of the selected folder
        folder_list = os.listdir(selected_folder)
        for i, folder_name in enumerate(folder_list):
            folder_button = tk.Button(canvas, text=folder_name, width=51, height=2, command=lambda folder=folder_name: self.open_folder(selected_folder, folder), bg="#FF69B4")
            folder_button.pack(side=tk.TOP, pady=5)

        # Update canvas properties
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        # Bind the scroll event to the canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")

        canvas.bind_all("<MouseWheel>", on_scroll)

        
    def home(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.logo = tk.Label(self.frame, text="Logo", width=20, height=3, bg="#FF69B4")
        self.logo.place(x=10,y=10)
        self.setting = tk.Button(self.frame, text="Cài đặt", width=20, height=3, bg="#FF69B4")
        self.setting.place(x=157,y=10)
        self.contact = tk.Button(self.frame, text="Liên hệ", width=20, height=3, bg="#FF69B4")
        self.contact.place(x=307,y=10)
        self.infomation = tk.Button(self.frame, text="Giới thiệu phần mềm", width=20, height=3, bg="#FF69B4")
        self.infomation.place(x=457,y=10)

    def cam(self, cam_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Cam đang chạy", height=2, width=177, font="large_font", bg="pink").place(x=10, y=10)
        tk.Label(self.frame, text="Danh sách máy hoạt động", height=2, width=40, font="large_font", bg="pink").place(x=10, y=50)

        canvas = tk.Canvas(self.frame, bg="pink", height=880)  
        canvas.place(x=8, y=90)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=380, y=90, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        cam_list = [0 for _ in range(cam_num)]
        for i in range(cam_num):
            cam_list[i] = tk.Button(cam_frame, text=f"Cam thứ {i+1}", width=51, height=2, command=self.show_cam, bg="#FF69B4")
            cam_list[i].pack(side=tk.TOP, pady=5)

        cam_frame.update_idletasks()  # Cập nhật cam_frame để có chiều cao chính xác cho canvas

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn

        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")
            canvas.bind_all("<MouseWheel>", on_scroll)

    def history(self,folder_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Lịch sử", height=2, width=177, font="large_font", bg="pink").place(x=10, y=10)
        tk.Label(self.frame, text="Nhập số báo danh", height=2, width=40, font="large_font", bg="#FFF0F5").place(x=900, y=52)
        tk.Label(self.frame, text="Danh sách thư mục", height=2, width=40, font="large_font", bg="pink").place(x=10, y=50)
        
        self.search = tk.Entry(self.frame, width=80)
        self.search.place(x=1000,y=90)
        
        canvas = tk.Canvas(self.frame, bg="pink", height=880)  
        canvas.place(x=10, y=90)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=380, y=90, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)
        
        folder_list = [0 for _ in range(folder_num)]
        for i in range(folder_num):
            folder_list[i] = tk.Button(cam_frame, text=f"folder thứ {i+1}", width=51, height=2, command=self.show_cam, bg="#FF69B4")
            folder_list[i].pack(side=tk.TOP, pady=5)

        search_button=tk.Button(self.frame, text="Tìm kiếm",height=1, command=lambda: self.show_folder(self.search,folder_list,canvas))
        search_button.place(x=1500,y=90)
        
        cam_frame.update_idletasks()  # Cập nhật cam_frame để có chiều cao chính xác cho canvas

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn
        
        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")
            canvas.bind_all("<MouseWheel>", on_scroll)

        
        
    def Sever_UI(self,screen_width,screen_height,cam_num,folder_num):
        self.Sx_position = -10
        self.Sy_position = 0

        self.root_width = screen_width 
        self.root_height = screen_height
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Sx_position}+{self.Sy_position}")

        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.top_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF66CC").pack(fill=tk.X)

        self.left_frame = tk.Frame(self.root, bg="pink")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.home_button = tk.Button(self.left_frame, text="Trang chủ", width=40, height=3,command=self.home, bg="#FF69B4")
        self.home_button.pack(side=tk.TOP)
        self.cam_button = tk.Button(self.left_frame, text="Cam đang chạy", width=40, height=3,command=lambda: self.cam(cam_num), bg="#FF69B4")
        self.cam_button.pack(side=tk.TOP)
        self.history_button = tk.Button(self.left_frame, text="Lịch sử", width=40, height=3,command=lambda: self.history(folder_num), bg="#FF69B4")
        self.history_button.pack(side=tk.TOP)
        
        
        self.frame = tk.Frame(self.root, bg="#FFF0F5")
        self.frame.pack(fill=tk.BOTH, expand=True)

    def First_time_UI(self,screen_width,screen_height):
        self.Sx_position = screen_width//2 - 400
        self.Sy_position = screen_height//2-400

        self.root_width = 400 
        self.root_height = 400
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Sx_position}+{self.Sy_position}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = UI_UX(root,"Sv",100, 100)
    root.mainloop()
