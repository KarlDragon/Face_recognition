import tkinter as tk
import os
import cv2
import time
import socket
import struct
import threading
import numpy as np
from PIL import Image, ImageTk

class UI_UX:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.iconbitmap(default=r"C:\C++\Homeworks\project\Module_File\app_img\logo_app.ico")

class Server_UI(UI_UX):
    def __init__(self, root):
        self.is_sound = True
        self.Sound_off = ImageTk.PhotoImage(Image.open(r"app_img\Sound_off.jpg").resize((50, 40)))
        self.Sound_on = ImageTk.PhotoImage(Image.open(r"app_img\Sound_on.jpg").resize((50, 40)))
        self.tk_background = ImageTk.PhotoImage(Image.open(r"app_img\logo_THPT.jpg").resize((1700, 1000)))
        self.tk_logo = ImageTk.PhotoImage(Image.open(r"app_img\logo_app_jpg.jpg").resize((50, 50)))
        super().__init__(root)

    def setting(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting_button:
                widget.destroy()

        tk.Label(self.frame, text="Nhập thời gian đếm ngược", height=4, width=177, font="large_font", bg="pink").pack(side=tk.TOP)
        tk.Label(self.frame, text="Giờ: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=530, y=160)
        tk.Label(self.frame, text="Phút: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=730, y=160)
        tk.Label(self.frame, text="Giây: ", height=2, width=10, font="large_font", bg="#FFF0F5").place(x=930, y=160)
        tk.Label(self.frame, text="Âm thanh cảnh báo", height=2, width=20, font="large_font", bg="#FFF0F5").place(
            x=1240, y=160)

        self.time_h = tk.Entry(self.frame, width=10)
        self.time_h.configure(font=("Arial", 19))
        self.time_h.place(x=550, y=190)

        self.time_m = tk.Entry(self.frame, width=10)
        self.time_m.configure(font=("Arial", 19))
        self.time_m.place(x=750, y=190)

        self.time_s = tk.Entry(self.frame, width=10)
        self.time_s.configure(font=("Arial", 19))
        self.time_s.place(x=950, y=190)

        self.done_button = tk.Button(self.frame, text="Bắt đầu", width=20, height=3, command=self.run_clock, bg="#99FFFF")
        self.done_button.place(x=750, y=350)

        self.sound_button = tk.Button(self.frame, image=self.Sound_on, width=50, height=40, command=self.sound,
                                      bg="#99FFFF")
        self.sound_button.place(x=1300, y=200)

        if self.is_sound:
            self.sound_button.config(image=self.Sound_on)
        else:
            self.sound_button.config(image=self.Sound_off)

    def run_clock(self):
        # Implement this function if needed
        pass

    def sound(self):
        if self.is_sound:
            self.sound_button.config(image=self.Sound_off)
        else:
            self.sound_button.config(image=self.Sound_on)

        self.is_sound = not self.is_sound

    def contact(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting_button:
                widget.destroy()

    def information(self):
        for widget in self.frame.winfo_children():
            if widget != self.top_home_frame and widget != self.setting_button:
                widget.destroy()

    def cam(self, cam_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Cam đang chạy", height=2, width=177, bg="pink", font=("Arial", 15)).place(x=10, y=10)
        tk.Label(self.frame, text="Danh sách máy hoạt động", height=2, width=35, bg="pink",
                 font=("Arial", 15)).place(x=10, y=50)

        canvas = tk.Canvas(self.frame, bg="pink", height=880)
        canvas.place(x=8, y=100)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=390, y=100, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        cam_list = [0 for _ in range(cam_num)]
        lst = ['HuynhGiaThien_110256', 'DangHoangPhong_110357']
        for i in range(cam_num):
            cam_list[i] = tk.Button(cam_frame, text=f"Cam:{lst[i]}", width=35, height=1, command=self.show_cam,
                                    font=("Arial", 15), bg="#FF69B4")
            cam_list[i].pack(side=tk.TOP, pady=5)

        cam_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")

        canvas.bind_all("<MouseWheel>", on_scroll)

    def history(self, folder_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="Lịch sử", height=2, width=177, bg="pink", font=("Arial", 15)).place(x=10, y=10)
        tk.Label(self.frame, text="Nhập số báo danh", height=2, width=40, bg="#FFF0F5",
                 font=("Arial", 15)).place(x=900, y=62)
        tk.Label(self.frame, text="Danh sách thư mục", height=2, width=35, bg="pink",
                 font=("Arial", 15)).place(x=10, y=50)

        self.search = tk.Entry(self.frame, width=80)
        self.search.place(x=1000, y=100)

        canvas = tk.Canvas(self.frame, bg="pink", height=880)
        canvas.place(x=10, y=90)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=390, y=90, height=880)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        folder_list = [0 for _ in range(folder_num)]
        lst = ['HuynhGiaThien_11B12_110256', 'DangHoangPhong_11B12_110357']
        for i in range(folder_num):
            folder_list[i] = tk.Button(cam_frame, text=f"folder:{lst[i]}", width=35, height=1, command=self.show_cam,
                                       font=("Arial", 15), bg="#FF69B4")
            folder_list[i].pack(side=tk.TOP, pady=5)

        search_button = tk.Button(self.frame, text="Tìm kiếm", height=1,
                                  command=lambda: self.show_folder(self.search, folder_list, canvas))
        search_button.place(x=1500, y=90)

        cam_frame.update_idletasks()

        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")

        canvas.bind_all("<MouseWheel>", on_scroll)

    def show_cam(self):
        pass

    def show_folder(self, search, folder_list, canvas):
        index = int(search.get()) - 1

        for widget in canvas.winfo_children():
            widget.destroy()

        folder_list = os.listdir(selected_folder)
        for i, folder_name in enumerate(folder_list):
            folder_button = tk.Button(canvas, text=folder_name, width=51, height=2,
                                      command=lambda folder=folder_name: self.open_folder(selected_folder, folder),
                                      bg="#FF69B4")
            folder_button.pack(side=tk.TOP, pady=5)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")

        canvas.bind_all("<MouseWheel>", on_scroll)

    def open_folder(self, path, folder):
        pass

    def home(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, image=self.tk_background, height=1000, width=1900).place(x=-80, y=50)

        self.top_home_frame = tk.Frame(self.frame, bg="#FF69B4")
        self.top_home_frame.pack(side=tk.TOP, fill=tk.X)

        self.logo = tk.Label(self.top_home_frame, image=self.tk_logo, width=50, height=50, bg="#FF69B4")
        self.logo.pack(side=tk.LEFT)

        self.information_button = tk.Button(self.top_home_frame, text="Giới thiệu phần mềm", width=20, height=2,
                                           command=self.information, font=("Arial", 15), bg="#FF69B4")
        self.information_button.pack(side=tk.RIGHT)

        self.contact_button = tk.Button(self.top_home_frame, text="Về chúng tôi", width=15, height=2,
                                        command=self.contact, font=("Arial", 15), bg="#FF69B4")
        self.contact_button.pack(side=tk.RIGHT)

        self.setting_button = tk.Button(self.top_home_frame, text="Cài đặt", width=10, height=2, command=self.setting,
                                        font=("Arial", 15), bg="#FF69B4")
        self.setting_button.pack(side=tk.RIGHT)

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, conn, addr, path):
        ip_address, port_number = addr
        print(f"Connection from {addr}")
        folder_path = os.path.join(path, ip_address)
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

        conn.close()
        print(f"Connection from {addr} closed")

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)

    def start_server(self, path, IP, port, num):
        self.server_socket.bind((IP, port))
        self.server_socket.listen(num)

        print("Server is listening on port ")

        while True:
            conn, addr = self.server_socket.accept()

            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, path))
            client_thread.start()

if __name__ == "__main__":
    def run_gui_and_server(path, IP, port):
        root = tk.Tk()
        app = Server_UI(root)
        app.home()

        gui_thread = threading.Thread(target=root.mainloop)

        server_instance = Server()
        server_thread = threading.Thread(target=server_instance.start_server, args=(path, IP, port, 5))

        gui_thread.start()
        server_thread.start()

        def check_server_thread():
            if not server_thread.is_alive():
                root.destroy()
            else:
                root.after(100, check_server_thread)

        root.after(100, check_server_thread)
        gui_thread.join()

    path = r"C:\C++\Homeworks\project\e"
    IP = "192.168.1.185"
    port = 8888

    run_gui_and_server(path, IP, port)
