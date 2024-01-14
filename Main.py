import os
import cv2
import time
import queue
import socket
import struct
import threading
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_server(self, IP, port):
        self.client_socket.connect((IP, port))

    def disconnect_server(self):
        self.client_socket.close()

    def send_images(self, folder_path, name_file):
        for filename in os.listdir(folder_path):
            
            self.client_socket.sendall(name_file.encode('utf-8'))
            
            image_path = os.path.join(folder_path, filename)

            with open(image_path, 'rb') as file:
                image_data = file.read()

            size = struct.pack("!I", len(image_data))
            
            self.client_socket.sendall(size)
            self.client_socket.sendall(image_data)

            print(f"Sent image: {filename}")

            if not self.receive_acknowledgment():
                break

        print("All images sent successfully!")

    def receive_acknowledgment(self):
        ack_data = self.client_socket.recv(3)
        
        if ack_data != b"ACK":
            print("Error: Acknowledgment not received.")
            return False
        
        return True

    def send_folder_thread(self, path):
        try:
            client.send_images(path)  
        except Exception as e:
            print(f"Error in send_folder_thread: {e}")

class Sever:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def handle_client(self, conn, addr, path):
        ip_address, port_number = addr
        print(f"Connection from {addr}")
        folder_path=os.path.join(path, ip_address)
        self.create_folder(folder_path)
        while True:
            folder_name=conn.recv(1024).decode('utf-8')
            save_folder=os.path.join(folder_path, folder_name)
            self.create_folder(save_folder)
            # Receive the size of the image data
            size_data = conn.recv(4)
            if not size_data:
                break

            size = struct.unpack("!L", size_data)[0]

            # Receive image data
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

            # Send acknowledgment to the client
            conn.sendall(b"ACK")

        conn.close()
        print(f"Connection from {addr} closed")

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)
        
    def start_server(self,path,IP,port,num):
        
        self.server_socket.bind(( IP, port ))
        self.server_socket.listen(num) 

        print("Server is listening on port ")

        while True:
            conn, addr = self.server_socket.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, path))
            client_thread.start()

class UI_UX:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.mode=None
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        check_button=False
        self.is_sound=True
        self.is_client_main=False
        self.is_client_UI=False
        self.Sound_off = ImageTk.PhotoImage(Image.open(r"Sound_off.jpg").resize((50,40)))
        self.Sound_on = ImageTk.PhotoImage(Image.open(r"Sound_on.jpg").resize((50,40)))
        self.is_done=False
        self.ui_update_interval =100
        self.tk_background = ImageTk.PhotoImage(Image.open(r"logo_THPT.jpg").resize((1700,1000)))
        self.tk_logo = ImageTk.PhotoImage(Image.open(r"logo_app_jpg.jpg").resize((50,50)))
        self.root.iconbitmap(default=r"logo_app.ico")
        self.sv = Sever()
        
    def Client_main(self):
        self.is_done=True
            
        
    def Client_UI(self,img):
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
            
        if self.is_client_UI and self.is_done:
            self.photo_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            if not self.is_client_main:
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
                self.is_client_main=True
            else:
                self.back_ground.configure(image=self.photo_image)
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
            
        tk.Label(self.frame, image=self.tk_background, height=1000, width=1900).place(x=-80, y=50)
        
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

        cam_list = [0 for _ in range(cam_num)]
        lst=['HuynhGiaThien_110256','DangHoangPhong_110357']
        for i in range(cam_num):
            cam_list[i] = tk.Button(cam_frame, text=f"Cam:{lst[i]}", width=35, height=1, command=self.show_cam,font=("Arial", 15), bg="#FF69B4")
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
        
        folder_list = [0 for _ in range(folder_num)]
        lst=['HuynhGiaThien_11B12_110256','DangHoangPhong_11B12_110357']
        for i in range(folder_num):
            folder_list[i] = tk.Button(cam_frame, text=f"folder:{lst[i]}", width=35, height=1, command=self.show_cam,font=("Arial", 15), bg="#FF69B4")
            folder_list[i].pack(side=tk.TOP, pady=5)

        search_button=tk.Button(self.frame, text="Tìm kiếm",height=1, command=lambda: self.show_folder(self.search,folder_list,canvas))
        search_button.place(x=1500,y=90)
        
        cam_frame.update_idletasks()  

        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Xác định vùng cuộn
        
        # Bắt sự kiện cuộn để cuộn cả canvas
        def on_scroll(event):
            canvas.yview_scroll(-1 * event.delta // 120, "units")
            canvas.bind_all("<MouseWheel>", on_scroll)

        
        
    def Sever_UI(self,cam_num,folder_num):
        self.Sx_position = -10
        self.Sy_position = 0

        self.root_width = self.screen_width 
        self.root_height = self.screen_height
        
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
    def user_mode_button(self,mode):
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
        with open('information.txt','w') as f:
            mode=f.writelines(mode)
            f.writelines("\n")
            path=f.writelines(path.get())
            f.writelines("\n")
            IP=f.writelines(IP.get())
            f.writelines("\n")
            port=f.writelines(port.get())
        self.root.destroy()
        
    def First_time_UI(self):
        self.Sx_position = self.screen_width//2 - 300
        self.Sy_position = self.screen_height//2-200

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

        7
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
        
class FaceRecognition:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.queue = queue.Queue()  
        self.stop_event = threading.Event()
        self.warning_count = 1
        self.recognition = False
        self.x_border = self.y_border = 1e6
        self.x1_border = self.y1_border = 0
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self.current_folder_path = None  
        self.ui_update_interval = 100  # in milliseconds
        self.update_ui_event = threading.Event()

        self.set_camera_properties(1, 1)

        self.UI=UI_UX()

    def set_camera_properties(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)

    def put_text_on_frame(self, frame, text, count=0):
        text = f"{text}!"
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (50, 50 + 10 * count)
        font_scale = 1
        font_thickness = 2
        font_color = (0, 0, 255)
        cv2.putText(frame, text, position, font, font_scale, font_color, font_thickness)

    def take_photos(self, frame, timestamp, folder_path):
        file_path = os.path.join(folder_path, f"{timestamp}.jpg")
        cv2.imwrite(file_path, frame)

    def run_face_recognition(self, path, IP, port):
        try:
            client = Client()
            client.connect_server(IP, port)
             while not self.stop_event.is_set():
                while self.cap.isOpened():
                    ret, frame = self.cap.read()
                    size = frame.shape

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                               flags=cv2.CASCADE_SCALE_IMAGE)
                    noses = self.nose_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10),
                                                               flags=cv2.CASCADE_SCALE_IMAGE)

                    if len(faces) > 0:
                        self.recognition = True
                        first_face = faces[0]
                    else:
                        first_face = None
                        self.put_text_on_frame(frame, 'Can not recognize face', 1)

                    if len(noses) > 0:
                        first_nose = noses[0]
                    else:
                        first_nose = None

                    if first_face is not None and first_nose is not None:
                        x_face, y_face, w_face, h_face = first_face
                        x1_face = x_face + w_face
                        y1_face = y_face + h_face
                        xmd_face = round(x_face + w_face / 2)

                        x_nose, y_nose, w_nose, h_nose = first_nose
                        xmd_nose, ymd_nose = x_nose + w_nose // 2, y_nose + h_nose // 2

                        self.x_border = round(min((size[1] - w_face) / 2 + 5, self.x_border))
                        self.y_border = round(min((size[0] - h_face) / 2 + 5, self.y_border))
                        self.x1_border = round(max((size[1] + w_face) / 2 + 5, self.x1_border))
                        self.y1_border = round(max((size[0] + h_face) / 2 + 5, self.y1_border))

                        if not (self.x_border < x_face and self.y_border < y_face and
                                self.x1_border > x1_face and self.y1_border > y1_face):

                            cv2.rectangle(frame, (self.x_border, self.y_border), (self.x1_border, self.y1_border),
                                          (0, 0, 255), 1)
                            cv2.rectangle(frame, (x_nose, y_nose), (x_nose + w_nose, y_nose + h_nose), (255, 0, 0), 1)
                            cv2.rectangle(frame, (x_face, y_face), (x1_face, y1_face), (0, 255, 0), 1)

                            self.put_text_on_frame(frame, 'Please move your face into frame!', 1)
                    if self.recognition:
                        distance = abs(xmd_face - xmd_nose)

                        if distance > 4 or first_face is None:
                            self.put_text_on_frame(frame, 'Warning!!', 3)
    
                            time_now = time.strftime("(%d-%m-%Y) (%H-%M-%S)", time.localtime())
    
                            if not self.current_folder_path:
                                self.current_folder_path = os.path.join(path, f'Warning_{self.warning_count}')
                                self.create_folder(self.current_folder_path)
    
                                if os.path.exists(os.path.join(path, f'Warning_{self.warning_count - 1}')):
                                    send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count - 1}'),f'Warning_{self.warning_count - 1}'),)
            
                                    send_thread.start()
    
                                self.warning_count += 1
    
                            self.take_photos(frame, time_now, self.current_folder_path)

                        else:
                            # Prepare for the next folder
                            self.current_folder_path = None  # Reset to None
                    #cv2.imshow("F",frame)
                    self.queue.put(frame)
                    
                    #if cv2.waitKey(25) & 0xFF == ord('q'):
                        send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count - 1}'),f'Warning_{self.warning_count - 1}'),)
                        send_thread.start()
                        #break
        
                # Release the video capture object
                self.cap.release()

                # Closes all the frames
                cv2.destroyAllWindows()

            #client.disconnect_server()  # Corrected method name

        except Exception as e:
            print(f"Error when trying to open camera: {e}")
            input("Press any key to quit")
            exit()
    
        # Start a separate thread for updating the UI
    def start_face_recognition_thread(self, path, IP, port):
        # Create a thread for face recognition
        self.face_recognition_thread = threading.Thread(target=self.run_face_recognition, args=(path, IP, port))
        self.face_recognition_thread.start()

        # Start a separate thread for updating the UI
        self.update_ui_thread = threading.Thread(target=self.update_ui)
        self.update_ui_thread.start()

    def update_ui(self):
        while not self.stop_event.is_set():
            try:
                frame = self.queue.get(timeout=1)  # Get the frame from the queue
                # Update the UI with the frame
                self.UI.root.after(self.UI.ui_update_interval, lambda: self.UI.Client_UI(frame))

            except queue.Empty:
                break
                # Ignore queue empty exception
        # Perform any cleanup or final UI updates

    def stop_threads(self):
        self.stop_event.set()  # Set the event to signal threads to stop
        self.face_recognition_thread.join()  # Wait for the face recognition thread to finish
        self.update_ui_thread.join()  # Wait for the update UI thread to finish
        
if __name__ == "__main__":
    is_txt=os.path.exists('information.txt')
    if is_txt:
        with open('information.txt','r') as f:
            mode=f.readline().replace('\n', '')
            path=f.readline().replace('\n', '')
            IP=f.readline().replace('\n', '')
            port=int(f.readline())
            
        if mode=="Cl":
            app=FaceRecognition()
            app.start_face_recognition_thread(path, IP, port)
            app.UI.root.mainloop()  # Start the main UI loop

            # When the UI loop exits (e.g., window is closed), stop the threads
            app.stop_threads()
        if mode=="Sv":
            app=UI_UX()
            app.Sever_UI(2,2)
    else:
        app=UI_UX()
        app.First_time_UI()
