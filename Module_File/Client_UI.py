from UI_UX import UI_UX
import tkinter as tk
from PIL import Image, ImageTk

class Client_UI(UI_UX):
    def __init__(self,root):
        self.is_client_main=False
        self.is_client_UI=False
        self.is_done=False
        self.photo_image=None
        super().__init__(root)

    def img_config(self):
        self.back_ground.configure(image=self.photo_image)
        
    def Client_main(self):
        name = self.name_user.get()
        num = self.user_num.get()
        class_ = self.user_class.get()
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        self.back_ground = tk.Label(self.frame, image=self.photo_image)
        self.back_ground.pack(fill=tk.BOTH, expand=True)
        
        time_left = "00:45:00"
        
        tk.Label(self.frame, text=time_left, font=("Helvetica", 24)).place(x=450, y=10)
        tk.Label(self.frame, text=f"Tên: {name} Lớp: {class_} Số báo danh: {num}", font=("Helvetica", 15)).place(x=0, y=270)


    
    def Cl_UI(self,img):
        if not self.is_client_UI:
            self.Cx_position = self.screen_width * 2 // 3
            self.Cy_position = 0

            self.root_width = self.screen_width // 3
            self.root_height = self.screen_height // 3
            
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
            self.is_client_UI=True
            
        else:
            self.photo_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            self.img_config()
            

