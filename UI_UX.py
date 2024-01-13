import tkinter as tk
from PIL import Image, ImageTk

class UI_UX:
    def __init__(self, root, mode,cam_num,folder_num):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.mode=None
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        check_button=False
        self.is_sound=True
        self.Sound_off = ImageTk.PhotoImage(Image.open(r"Sound_off.jpg").resize((50,40)))
        self.Sound_on = ImageTk.PhotoImage(Image.open(r"Sound_on.jpg").resize((50,40)))
        
        if mode=="Fi":
            self.First_time_UI(screen_width,screen_height)
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

        time_left = "00:45:00"
        tk.Label(self.frame, text=time_left, bg="pink", font=("Helvetica", 24)).place(x=450, y=10)

        tk.Label(self.frame, text=f"Tên: {name} Lớp: {class_} Số báo danh: {num}", bg="pink", font=("Helvetica", 15)).place(x=0, y=270)

    def Client_UI(self,screen_width,screen_height):
        self.Cx_position = screen_width * 2 // 3
        self.Cy_position = 0

        self.root_width = screen_width // 3
        self.root_height = screen_height // 3
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Cx_position}+{self.Cy_position}")

        self.top_frame = tk.Frame(self.root, bg="#FF69B4")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.top_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#99CCFF").pack(fill=tk.X)

        self.frame = tk.Frame(self.root, bg="#FFFAEC")
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Họ và tên:", height=2, bg="#FFFAEC",font=("Arial", 14)).place(x=50, y=0)
        
        self.name_user = tk.Entry(self.frame, width=50)
        self.name_user.place(x=50, y=self.root_height*1//7 -10 )
        self.name_user.config(highlightthickness=1, highlightbackground="black")
        
        tk.Label(self.frame, text="Số báo danh:", height=2, bg="#FFFAEC",font=("Arial", 14)).place(x=50, y=120)
        
        self.user_num = tk.Entry(self.frame, width=50)
        self.user_num.place(x=50, y=160)
        self.user_num.config(highlightthickness=1, highlightbackground="black")
        
        tk.Label(self.frame, text="Lớp:", height=1, bg="#FFFAEC",font=("Arial", 14)).place(x=50, y=70)
        
        self.user_class = tk.Entry(self.frame, width=50)
        self.user_class.border_radius = 360
        self.user_class.place(x=50, y=100)
        self.user_class.config(highlightthickness=1, highlightbackground="black")
    
        
        self.login_button = tk.Button(self.frame, text="Hoàn tất", width=10, height=1, command=self.Client_main, bg="#3366CC",font=("Arial", 15,"bold"))
        self.login_button.place(x=225, y=self.root_height * 5 // 7 - 20)
        
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

    #functions for home()

    def run_clock(self):
        pass

    def sound(self):
        if self.is_sound:
            self.sound_button.config(image=self.Sound_off)
            
        else:
            self.sound_button.config(image=self.Sound_on)

        self.is_sound= not self.is_sound
    
    def setting(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting:  
                widget.destroy()

        tk.Label(self.frame, text="Nhập thời gian đếm ngược", height=4, width=177, font="large_font", bg="pink").pack(side=tk.TOP)
        tk.Label(self.frame, text="Giờ: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=530,y=160)
        tk.Label(self.frame, text="Phút: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=730,y=160)
        tk.Label(self.frame, text="Giây: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=930,y=160)
        tk.Label(self.frame, text="Âm thanh cảnh báo", height=2, width=20, font="large_font", bg="#FFF0F5").place(x=1240,y=160)
        
        self.time_h = tk.Entry(self.frame, width=10)
        self.time_h.configure(font=("Arial", 19))  
        self.time_h.place(x=550,y=190)

        self.time_m = tk.Entry(self.frame, width=10)
        self.time_m.configure(font=("Arial", 19))  
        self.time_m.place(x=750,y=190)

        self.time_s = tk.Entry(self.frame, width=10)
        self.time_s.configure(font=("Arial", 19))  
        self.time_s.place(x=950,y=190)

        self.done_button = tk.Button(self.frame, text="Bắt đầu", width=20, height=3, command=self.run_clock, bg="#99FFFF")
        self.done_button.place(x=750,y=350)

        self.sound_button = tk.Button(self.frame, image=self.Sound_on, width=50, height=40, command=self.sound, bg="#99FFFF")       
        self.sound_button.place(x=1300,y=200)
        
        if self.is_sound:
            self.sound_button.config(image=self.Sound_on)
        else:
            self.sound_button.config(image=self.Sound_off)
        
    def contact(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting:  # Preserve top_home_frame and its contents
                widget.destroy()

    def information(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting:  # Preserve top_home_frame and its contents
                widget.destroy()

    #functions for Sever_UI
    def home(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.top_home_frame = tk.Frame(self.frame, bg="#FF69B4")
        self.top_home_frame.pack(side=tk.TOP, fill=tk.X)

        self.logo = tk.Label(self.top_home_frame, text="Logo", width=20, height=3, bg="#FF69B4")
        self.logo.pack(side=tk.LEFT)

        self.information_button = tk.Button(self.top_home_frame, text="Giới thiệu phần mềm", width=20, height=2, command=self.information,font=("Arial", 15), bg="#FF69B4")
        self.information_button.pack(side=tk.RIGHT)

        self.contact_button = tk.Button(self.top_home_frame, text="Về chúng tôi", width=15, height=2, command=self.contact,font=("Arial", 15), bg="#FF69B4")
        self.contact_button.pack(side=tk.RIGHT)

        self.setting_button = tk.Button(self.top_home_frame, text="Cài đặt", width=10, height=2, command=self.setting,font=("Arial", 15), bg="#FF69B4")
        self.setting_button.pack(side=tk.RIGHT)

    def cam(self, cam_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Cam đang chạy", height=2, width=177, bg="pink",font=("Arial", 15)).place(x=10, y=10)
        tk.Label(self.frame, text="Danh sách máy hoạt động", height=2, width=40, bg="pink",font=("Arial", 15)).place(x=10, y=50)

        canvas = tk.Canvas(self.frame, bg="pink", height=880)  
        canvas.place(x=8, y=90)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=380, y=90, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        cam_list = [0 for _ in range(cam_num)]
        for i in range(cam_num):
            cam_list[i] = tk.Button(cam_frame, text=f"Cam thứ {i+1}", width=51, height=2, command=self.show_cam,font=("Arial", 15), bg="#FF69B4")
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
        tk.Label(self.frame, text="Lịch sử", height=2, width=177, bg="pink",font=("Arial", 15)).place(x=10, y=10)
        tk.Label(self.frame, text="Nhập số báo danh", height=2, width=40, bg="#FFF0F5",font=("Arial", 15)).place(x=900, y=52)
        tk.Label(self.frame, text="Danh sách thư mục", height=2, width=35, bg="pink",font=("Arial", 15)).place(x=10, y=50)
        
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
            folder_list[i] = tk.Button(cam_frame, text=f"folder thứ {i+1}", width=35, height=2, command=self.show_cam,font=("Arial", 15), bg="#FF69B4")
            folder_list[i].pack(side=tk.TOP, pady=5)

        search_button=tk.Button(self.frame, text="Tìm kiếm",height=1, command=lambda: self.show_folder(self.search,folder_list,canvas))
        search_button.place(x=1500,y=90)
        
        cam_frame.update_idletasks()  

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
        self.home_button = tk.Button(self.left_frame, text="Trang chủ", width=15, height=2,command=self.home,font=("Arial", 15), bg="#FF69B4")
        self.home_button.pack(side=tk.TOP)
        self.cam_button = tk.Button(self.left_frame, text="Cam đang chạy", width=15, height=2,command=lambda: self.cam(cam_num),font=("Arial", 15), bg="#FF69B4")
        self.cam_button.pack(side=tk.TOP)
        self.history_button = tk.Button(self.left_frame, text="Lịch sử", width=15, height=2,command=lambda: self.history(folder_num),font=("Arial", 15), bg="#FF69B4")
        self.history_button.pack(side=tk.TOP)
        
        
        self.frame = tk.Frame(self.root, bg="#FFF0F5")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.home()

    #UI for the first
    def user_mode(self,mode):
        if mode=="Sv":
            self.mode_button_sv.config(relief=tk.SUNKEN)
            self.mode_button_cl.config(relief=tk.RAISED)
            self.mode=mode
            return self.mode
        if mode=="Cl":
            self.mode_button_cl.config(relief=tk.SUNKEN)
            self.mode_button_sv.config(relief=tk.RAISED)
            self.mode=mode
            return self.mode
        
    def user_infor(self,mode,path,IP,port):
        print(mode)
        print(path.get())
        print(IP.get())
        print(port.get())
        self.root.destroy()
        root = tk.Tk()
        app = UI_UX(root,mode,100, 100)
        root.mainloop()
        
    def First_time_UI(self,screen_width,screen_height):
        self.Sx_position = screen_width//2 - 300
        self.Sy_position = screen_height//2-200

        self.root_width = 600 
        self.root_height = 400
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Sx_position}+{self.Sy_position}")

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill=tk.BOTH,expand=True)
        self.inf_frame = tk.Frame(self.frame, bg="white")
        self.inf_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.inf_frame, text="Nhập thông tin", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF69B4").pack(fill=tk.X)

        self.mode_frame = tk.Frame(self.frame, bg="white")
        self.mode_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.mode_frame, text="Bạn là: ", height=2,width=20, fg="black", font=("Helvetica", 15, "bold"), bg="white").pack(side=tk.LEFT,pady=10)
        
        self.mode_button_sv = tk.Button(self.mode_frame, text="Máy chủ", width=20, height=3,command=lambda: self.user_mode("Sv"), bg="#FF99CC")
        self.mode_button_sv.pack(side=tk.LEFT,pady=10)
        
        self.mode_button_cl = tk.Button(self.mode_frame, text="Máy khách", width=20, height=3,command=lambda: self.user_mode("Cl"), bg="#FF99CC")
        self.mode_button_cl.pack(side=tk.LEFT,pady=10)

        self.path_frame = tk.Frame(self.frame, bg="white")
        self.path_frame.pack(side=tk.TOP, fill=tk.X,pady=10)
        
        tk.Label(self.path_frame, text="                    Nhập đường dẫn: ", height=2, font="large_font", bg="white").pack(side=tk.LEFT)
        
        self.path = tk.Entry(self.path_frame, width=40, border_radius=5)
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
        
        self.mode_button = tk.Button(self.frame, text="Hoàn tất", width=20, height=3,command=lambda: self.user_infor(self.mode,self.path,self.IP,self.port), bg="#FF69B4")
        self.mode_button.pack(side=tk.TOP,pady=10)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = UI_UX(root,"Sv",100, 100)
    root.mainloop()
