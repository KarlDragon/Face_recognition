import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
import time
import socket
import struct
import threading
import numpy as np
import pickle
import sys
import queue
import subprocess
class UI_UX:
    def __init__(self, root):
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
        
class Server_UI(UI_UX):
    def __init__(self,root,path,IP,port,amount):
        check_button=False
        self.is_sound=True
        super().__init__(root)
        Sound_off_path=os.path.join(self.current_directory, 'app_img', 'Sound_off.jpg')
        self.Sound_off = ImageTk.PhotoImage(Image.open(Sound_off_path).resize((50,40)))
        Sound_on_path=os.path.join(self.current_directory, 'app_img', 'Sound_on.jpg')
        self.Sound_on = ImageTk.PhotoImage(Image.open(Sound_on_path).resize((50,40)))
        tk_logo_path=os.path.join(self.current_directory, 'app_img', 'logo_app_jpg.jpg')
        self.tk_logo = ImageTk.PhotoImage(Image.open(tk_logo_path).resize((50,50)))
        self.path=path
        self.IP=IP
        self.port=port
        self.amount=amount
        self.server = Server(self.path, self.IP, self.port,self.amount)
        self.back_ground = False
        self.image_queue = queue.Queue()
    
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

        self.time_frame = tk.Frame(self.frame, bg="#FFF0F5")
        self.time_frame.pack(side=tk.TOP,anchor=tk.NW,padx=120)

        tk.Label(self.time_frame, text="Giờ: ", height=2, width=10, font="large_font", bg="#FFF0F5").pack(side=tk.LEFT,padx=10)
        tk.Label(self.time_frame, text="Phút: ", height=2, width=10, font="large_font", bg="#FFF0F5").pack(side=tk.LEFT)
        tk.Label(self.time_frame, text="Giây: ", height=2, width=10, font="large_font", bg="#FFF0F5").pack(side=tk.LEFT)
        tk.Label(self.time_frame, text="Âm thanh cảnh báo", height=2, width=20, font="large_font", bg="#FFF0F5").pack(side=tk.LEFT)

        self.entry_frame = tk.Frame(self.frame, bg="#FFF0F5")
        self.entry_frame.pack(side=tk.TOP,anchor=tk.NW,padx=130)

        self.time_h = tk.Entry(self.entry_frame, width=5)
        self.time_h.configure(font=("Arial", 19))
        self.time_h.pack(side=tk.LEFT,padx=20)

        self.time_m = tk.Entry(self.entry_frame, width=5)
        self.time_m.configure(font=("Arial", 19))
        self.time_m.pack(side=tk.LEFT,padx=20)

        self.time_s = tk.Entry(self.entry_frame, width=5)
        self.time_s.configure(font=("Arial", 19))
        self.time_s.pack(side=tk.LEFT,padx=30)


        self.done_button = tk.Button(self.frame, text="Bắt đầu", width=20, height=3, command=self.run_clock, bg="#99FFFF")
        self.done_button.pack(side=tk.TOP,pady=50)

        self.sound_button = tk.Button(self.entry_frame, image=self.Sound_on, width=50, height=40, command=self.sound, bg="#99FFFF")       
        self.sound_button.pack(side=tk.TOP)
        
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
        
        self.competition_frame = tk.Frame(self.frame, bg="#FF69B4")
        self.competition_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.competition = tk.Label(self.competition_frame, text="CUỘC THI KHOA HỌC KĨ THUẬT CẤP TỈNH DÀNH CHO HỌC SINH TRUNG HỌC NĂM HỌC 2023-2024", width=200, height=5,font=("Helvetica",10,"bold"), bg="#FF69B4")
        self.competition.pack(side=tk.LEFT)

        self.top_home_frame_info = self.top_home_frame.winfo_geometry()
        self.top_home_frame_x, self.top_home_frame_y = map(int, self.top_home_frame_info.split('+')[1:3])

        self.competition_frame_info = self.competition_frame.winfo_geometry()
        self.competition_frame_x, self.competition_frame_y = map(int, self.competition_frame_info.split('+')[1:3])

        self.frame_info = self.frame.winfo_geometry()
        self.frame_info_x, self.frame_info_y = map(int, self.frame_info.split('+')[1:3])
        
        self.distance_x = self.root_width - self.frame_info_x
        self.distance_y = self.root_height - self.competition_frame_y - self.top_home_frame_y

        background_path = tk_logo_path=os.path.join(self.current_directory, 'app_img', 'home_bg.jpg')
        self.tk_background = ImageTk.PhotoImage(Image.open(background_path).resize((self.distance_x,self.distance_y)))
        tk.Label(self.frame, image=self.tk_background).pack(side=tk.TOP,fill=tk.BOTH, expand=True)

    def update_image_in_main_thread(self):
        try:
            img = self.image_queue.get_nowait()
            self.back_ground.configure(image=img)
            self.back_ground.image = img
        except queue.Empty:
            pass

        # Schedule the next update on the main thread after 100 milliseconds
        self.root.after(200, self.update_image_in_main_thread)

    def show_cam(self, key):
        try:
            self.display_image(key)  
            self.root.after(200, lambda: self.show_cam(key))
            self.update_image_in_main_thread()
        except Exception as e:
            print(f"Error in show_cam: {e}")

            
    def display_image(self, key):
        try:
            img = ImageTk.PhotoImage(
                Image.fromarray(
                    cv2.cvtColor(self.server.image_dict[key], cv2.COLOR_BGR2RGB)))
            # Put the image in the queue
            self.image_queue.put(img)

            # Schedule the next update after 100 milliseconds
            self.root.after(200, lambda: self.display_image(key))
        except Exception as e:
            print(f"Error displaying image: {e}")
            
    def cam(self, cam_num):
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.frame, text="Cam đang chạy", height=2, width=177, bg="pink",font=("Arial", 15)).pack(side=tk.TOP,fill=tk.X)
        tk.Label(self.frame, text="Danh sách máy hoạt động", height=2, width=25, bg="pink",font=("Arial", 15)).pack(side=tk.TOP,anchor=tk.NW)

        canvas = tk.Canvas(self.frame, bg="pink",width=280 )  
        canvas.pack(side=tk.LEFT,fill=tk.Y,anchor=tk.NW)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT,fill=tk.Y,anchor=tk.NW)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        self.back_ground = tk.Label(self.frame)
        self.back_ground.pack(fill=tk.BOTH, expand=True)
        
        for key, value in self.server.image_dict.items():
            if not any(btn["text"] == key for btn in cam_frame.winfo_children()):
                tk.Button(cam_frame,
                          text=key,
                          width=35,
                          height=1,
                          command=lambda: self.show_cam(key),
                          font=("Arial", 15),
                          bg="#FF69B4").pack(side=tk.TOP, pady=5)


        cam_frame.update_idletasks()  # Cập nhật cam_frame để có chiều cao chính xác cho canvas

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn

        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")
            canvas.bind_all("<MouseWheel>", on_scroll)

    def search_folder(self, search, folder_list, canvas):
        pass

    def show_folder(self, value):
        subprocess.Popen(['explorer', '/n, /e, ', value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.frame.update()

    def history(self, folder_num):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Lịch sử", height=2, width=177, bg="pink", font=("Arial", 15)).pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.frame, text="Nhập số báo danh", height=2, width=40, bg="#FFF0F5", font=("Arial", 15)).place(x=900, y=62)
        tk.Label(self.frame, text="Danh sách thư mục", height=2, width=25, bg="pink", font=("Arial", 15)).pack(side=tk.TOP,
                                                                                                           anchor=tk.NW)

        self.search = tk.Entry(self.frame, width=80)
        self.search.place(x=1000, y=100)

        canvas = tk.Canvas(self.frame, bg="pink",width=280 )  
        canvas.pack(side=tk.LEFT,fill=tk.Y,anchor=tk.NW)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT,fill=tk.Y,anchor=tk.NW)

        canvas.configure(yscrollcommand=scrollbar.set)

        cam_frame = tk.Frame(canvas, bg="pink")
        canvas.create_window((0, 0), window=cam_frame, anchor=tk.NW)

        search_button = tk.Button(self.frame, text="Tìm kiếm", height=1,
                                  command=lambda: self.search_folder(self.search, folder_list, canvas))
        search_button.place(x=1500, y=90)

        self.bg_fr = tk.Frame(self.frame, bg="#FFF0F5")
        self.bg_fr.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        for key, value in self.server.user_path.items():
            if not any(btn["text"] == key for btn in cam_frame.winfo_children()):
                tk.Button(cam_frame,
                          text=key,
                          width=35,
                          height=1,
                          command=lambda: self.show_folder(value),  # Truyền tham số cho hàm
                          font=("Arial", 15),
                          bg="#FF69B4").pack(side=tk.TOP, pady=5)

        cam_frame.update_idletasks()

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn

        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")

        canvas.bind_all("<MouseWheel>", on_scroll)

        # Bỏ sự kiện cuộn khi kết thúc hàm
        canvas.unbind_all("<MouseWheel>")
        
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
        
        
        threading.Thread(target=self.server.start_server).start()

class VideoThread(threading.Thread):
    def __init__(self, conn, user_cam, image_dict, shared_lock):
        super().__init__()
        self.conn = conn
        self.user_cam = user_cam
        self.image_dict = image_dict
        self.shared_lock = shared_lock

    def run(self):
        while True:
            with self.shared_lock:
                data = b""
                payload_size = struct.calcsize("L")
                while len(data) < payload_size:
                    packet = self.conn.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.conn.recv(4 * 1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data)
                self.image_dict[self.user_cam] = frame

class FolderThread(threading.Thread):
    def __init__(self, conn, folder_path, shared_lock):
        super().__init__()
        self.conn = conn
        self.folder_path = folder_path
        self.shared_lock = shared_lock

    def run(self):
        while True:
            with self.shared_lock:
                folder_name = self.conn.recv(1024).decode('utf-8')
                save_folder = os.path.join(self.folder_path, folder_name)
                print(save_folder)
                self.create_folder(save_folder)

                size_data = self.conn.recv(4)
                if not size_data:
                    break

                size = struct.unpack("!L", size_data)[0]

                image_data = b""
                while len(image_data) < size:
                    chunk = self.conn.recv(size - len(image_data))
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

                self.conn.sendall(b"ACK")

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)
            
class Server:
    def __init__(self,path,IP,port,amount):
        self.path=path
        self.IP=IP
        self.port=port
        self.amount=amount
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.image_dict={}
        self.user_path={}
        self.shared_lock = threading.Lock()
        
    def handle_client(self, conn, addr):
        print(conn)
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

        user_folder=f"{name}_{class_}_{num}"
        user_cam=f"{name}_{class_}"
        
        folder_path = os.path.join(self.path, user_folder)
        self.create_folder(folder_path)
        
        video_thread = VideoThread(conn, user_cam, self.image_dict, self.shared_lock)
        folder_thread = FolderThread(conn, folder_path, self.shared_lock)
        self.user_path[user_folder]=folder_path
            
        video_thread.start()
        folder_thread.start()

        video_thread.join()
        folder_thread.join()

        conn.close()
        print(f"Connection from {addr} closed")

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

def run_gui_sv(path,IP,port,amount):
    root = tk.Tk()
    app = Server_UI(root,path,IP,port,amount)
    app.SV_UI(amount)
    root.mainloop()
