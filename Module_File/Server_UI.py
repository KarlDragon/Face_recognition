import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
import time
import socket
import struct
import threading
import numpy as np

class UI_UX:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.iconbitmap(default=r"C:\Python32\CV2\Face_recognition-main\Module_File\app_img\logo_app.ico")
        
class Server_UI(UI_UX):
    def __init__(self,root,path,IP,port,amount):
        check_button=False
        self.is_sound=True
        self.Sound_off = ImageTk.PhotoImage(Image.open(r"C:\Python32\CV2\Face_recognition-main\Module_File\app_img\Sound_off.jpg").resize((50,40)))
        self.Sound_on = ImageTk.PhotoImage(Image.open(r"C:\Python32\CV2\Face_recognition-main\Module_File\app_img\Sound_on.jpg").resize((50,40)))
        self.tk_background = ImageTk.PhotoImage(Image.open(r"C:\Python32\CV2\Face_recognition-main\Module_File\app_img\home_bg.jpg").resize((1000,600)))
        self.tk_logo = ImageTk.PhotoImage(Image.open(r"C:\Python32\CV2\Face_recognition-main\Module_File\app_img\logo_app_jpg.jpg").resize((50,50)))
        self.path=path
        self.IP=IP
        self.port=port
        self.amount=amount
        self.client_buttons = []
        super().__init__(root)

    def show_cam(self):
        pass

    def show_folder(self, search, folder_list, canvas):
        index = int(search.get()) - 1

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

        self.is_sound = not self.is_sound
    
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

        self.logo = tk.Label(self.top_home_frame, image=self.tk_logo, width=50, height=50, bg="#FF69B4")
        self.logo.pack(side=tk.LEFT)

        self.information_button = tk.Button(self.top_home_frame, text="Giới thiệu phần mềm", width=20, height=2, command=self.information,font=("Arial", 15), bg="#FF69B4")
        self.information_button.pack(side=tk.RIGHT)

        self.contact_button = tk.Button(self.top_home_frame, text="Về chúng tôi", width=15, height=2, command=self.contact,font=("Arial", 15), bg="#FF69B4")
        self.contact_button.pack(side=tk.RIGHT)

        self.setting_button = tk.Button(self.top_home_frame, text="Cài đặt", width=10, height=2, command=self.setting,font=("Arial", 15), bg="#FF69B4")
        self.setting_button.pack(side=tk.RIGHT)
        
        self.competition = tk.Frame(self.frame, bg="#FF69B4")
        self.competition.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.competition = tk.Label(self.competition, text="CUỘC THI KHOA HỌC KĨ THUẬT CẤP TỈNH DÀNH CHO HỌC SINH TRUNG HỌC NĂM HỌC 2023-2024", width=200, height=5,font=("Helvetica",10,"bold"), bg="#FF69B4")
        self.competition.pack(side=tk.LEFT)
        
        tk.Label(self.frame, image=self.tk_background).pack(side=tk.TOP,fill=tk.BOTH)

    def update_client_buttons(self, name, num, class_):
        button_text = f"Cam: {name}_{class_}_{num}"
        self.client_buttons.append(button_text)
        print(self.client_buttons)
        
    def cam(self, cam_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Cam đang chạy", height=2, width=177, bg="pink",font=("Arial", 15)).place(x=10, y=10)
        tk.Label(self.frame, text="Danh sách máy hoạt động", height=2, width=35, bg="pink",font=("Arial", 15)).place(x=10, y=50)

        canvas = tk.Canvas(self.frame, bg="pink", height=880)  
        canvas.place(x=8, y=100)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=390, y=100, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)


        for i in range(len(self.client_buttons)):
            
            tk.Button(cam_frame, text=f"Cam:{self.client_buttons[i]}", width=35, height=1, command=self.show_cam,font=("Arial", 15), bg="#FF69B4").pack(side=tk.TOP, pady=5)


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
        tk.Label(self.frame, text="Nhập số báo danh", height=2, width=40, bg="#FFF0F5",font=("Arial", 15)).place(x=900, y=62)
        tk.Label(self.frame, text="Danh sách thư mục", height=2, width=35, bg="pink",font=("Arial", 15)).place(x=10, y=50)
        
        self.search = tk.Entry(self.frame, width=80)
        self.search.place(x=1000,y=100)
        
        canvas = tk.Canvas(self.frame, bg="pink", height=880)  
        canvas.place(x=10, y=90)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=390, y=90, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)
        
        folder_list = [None for _ in range(folder_num)]
        for i in range(folder_num):
            folder_list[i] = tk.Button(cam_frame, text=f"folder:{folder_list[i]}", width=35, height=1, command=self.show_cam,font=("Arial", 15), bg="#FF69B4")
            folder_list[i].pack(side=tk.TOP, pady=5)

        search_button=tk.Button(self.frame, text="Tìm kiếm",height=1, command=lambda: self.show_folder(self.search,folder_list,canvas))
        search_button.place(x=1500,y=90)
        
        cam_frame.update_idletasks()  

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn
        
        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")
            canvas.bind_all("<MouseWheel>", on_scroll)

        
        
    def SV_UI(self,amount):
        self.Sx_position = -10
        self.Sy_position = 0

        self.root_width = self.screen_width 
        self.root_height = self.screen_height-50
        
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Sx_position}+{self.Sy_position}")

        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.top_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black", font=("Helvetica", 15, "bold"), bg="#FF66CC").pack(fill=tk.X)
        self.left_frame = tk.Frame(self.root, bg="pink")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.home_button = tk.Button(self.left_frame, text="Trang chủ", width=15, height=2,command=self.home,font=("Arial", 15), bg="#FF69B4")
        self.home_button.pack(side=tk.TOP)
        
        self.cam_button = tk.Button(self.left_frame, text="Cam đang chạy", width=15, height=2,command=lambda: self.cam(amount),font=("Arial", 15), bg="#FF69B4")
        self.cam_button.pack(side=tk.TOP)
        
        self.history_button = tk.Button(self.left_frame, text="Lịch sử", width=15, height=2,command=lambda: self.history(amount),font=("Arial", 15), bg="#FF69B4")
        self.history_button.pack(side=tk.TOP)
        
        
        self.frame = tk.Frame(self.root, bg="#FFF0F5")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.home()
        
        self.server = Server(self.path, self.IP, self.port, self.amount)
        self.server.set_server_ui_instance(self)  # Pass the Server_UI instance to the Server class
        
        threading.Thread(target=self.server.start_server).start()

class Server:
    def __init__(self,path,IP,port,amount):
        self.path=path
        self.IP=IP
        self.port=port
        self.amount=amount
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ui_instance = None

    def set_server_ui_instance(self, server_ui_instance):
        self.server_ui_instance = server_ui_instance
        
    def folder_thread(self, conn, addr, name, num, class_):
        try:
            main_folder = f"{name}_{class_}_{num}"
            folder_path = os.path.join(self.path, main_folder)

            if self.server_ui_instance:
                self.server_ui_instance.update_client_buttons(name, num, class_)

            self.create_folder(folder_path)

            while True:
                folder_name = conn.recv(1024).decode('utf-8')
                save_folder = os.path.join(folder_path, folder_name)
                self.create_folder(save_folder)

                size_data = conn.recv(4)
                if not size_data:
                    break

                size = struct.unpack("!L", size_data)[0]

                image_data = b""
                while len(image_data) < size:
                    chunk = conn.recv(size - len(image_data))
                    if not chunk:
                        break
                    image_data += chunk

                if not image_data:
                    break

                image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                filename = f"image_{time.time()}.jpg"
                image_path = os.path.join(save_folder, filename)
                cv2.imwrite(image_path, image)
                print(f"Image received and saved as: {image_path}")
                print(f"Recv: {len(image_data)} bytes")

                conn.sendall(b"ACK")

        except Exception as e:
            print(f"Error in handle_folder_thread: {e}")

        finally:
            conn.close()
            print(f"Connection from {addr} closed")

    def image_loop_thread(self, conn, addr, name, num, class_):
        try:
            while True:
                size_data = conn.recv(4)
                if not size_data:
                    break

                size = struct.unpack("!L", size_data)[0]

                image_data = b""
                while len(image_data) < size:
                    chunk = conn.recv(size - len(image_data))
                    if not chunk:
                        break
                    image_data += chunk

                if not image_data:
                    break

                image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                # Process the image as needed

        except Exception as e:
            print(f"Error in handle_image_loop_thread: {e}")

        finally:
            conn.close()
            print(f"Connection from {addr} closed")

    def handle_client(self, conn, addr):
        ip_address, port_number = addr
        print(f"Connection from {addr}")

        name = conn.recv(1024).decode('utf-8')
        print(f"Received name: {name}")

        time.sleep(1)  # Introduce a small delay to ensure proper order
        num = conn.recv(1024).decode('utf-8')
        print(f"Received num: {num}")

        time.sleep(1)  # Introduce a small delay to ensure proper order
        class_ = conn.recv(1024).decode('utf-8')
        print(f"Received class: {class_}")

        # Start the thread for handling folders
        folder_thread = threading.Thread(target=self.folder_thread, args=(conn, addr, name, num, class_))
        folder_thread.start()

        # Start the thread for handling the image loop
        image_loop_thread = threading.Thread(target=self.image_loop_thread, args=(conn, addr, name, num, class_))
        image_loop_thread.start()

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)

    def start_server(self):
        self.server_socket.bind((self.IP, self.port))
        self.server_socket.listen(self.amount)

        print("Server is listening on port ")

        while True:
            conn, addr = self.server_socket.accept()

            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

def run_gui_sv(path, IP, port, amount):
    root = tk.Tk()
    app = Server_UI(root, path, IP, port, amount)
    app.SV_UI(amount)
    root.mainloop()
