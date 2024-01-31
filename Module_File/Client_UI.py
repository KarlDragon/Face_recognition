import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
import time
import socket
import struct
import threading
import numpy as np
from queue import Queue 
import pickle
import sys
class Client:
    def __init__(self):
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.folder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock_send_images = threading.Lock()
        self.lock_video_loop = threading.Lock()
        
    def connect_server(self, IP, port):
        self.video_socket.connect((IP, port))
        time.sleep(1)
        self.folder_socket.connect((IP,port))
        
    def client_type(self):
        self.video_socket.sendall(b"VIDEO")
        time.sleep(1)
        self.folder_socket.sendall(b"FOLDER")
        
    def disconnect_server(self):
        self.video_socket.close()
        self.folder_socket.close()
        
    def send_images(self, folder_path, name_file):
        with self.lock_send_images:
            for filename in os.listdir(folder_path):
                
                self.folder_socket.sendall(name_file.encode('utf-8'))
                
                image_path = os.path.join(folder_path, filename)

                with open(image_path, 'rb') as file:
                    image_data = file.read()

                size = struct.pack("!I", len(image_data))
                
                self.folder_socket.sendall(size)
                self.folder_socket.sendall(image_data)

                print(f"Sent image: {filename}")

                if not self.receive_acknowledgment():
                    break

            print("All images sent successfully!")
        
    def video_loop(self,frame):
        with self.lock_video_loop:
            data = pickle.dumps(frame)
            # Gửi kích thước frame đến máy khách
            self.video_socket.sendall(struct.pack("L", len(data)) + data)

    def send_info_folder(self ,name,num,class_):
        try:
            self.folder_socket.sendall(name.encode('utf-8'))
            time.sleep(1)  
            self.folder_socket.sendall(num.encode('utf-8'))
            time.sleep(1)
            self.folder_socket.sendall(class_.encode('utf-8'))
            time.sleep(1)
            
            print(f"Sending {name}, {num}, {class_}")
            print("Sending info successfully!")

        except Exception as e:
            print(f"Error in send_info_folder: {e}")

    def send_info_video(self,name,class_):
        try:
            self.video_socket.sendall(name.encode('utf-8'))
            time.sleep(1)  
            self.video_socket.sendall(class_.encode('utf-8'))
            time.sleep(1)
            
            print(f"Sending {name},{class_} in video")
            print("Sending info successfully!")
            time.sleep(1)
        except Exception as e:
            print(f"Error in send_info_video: {e}")
            
    def receive_acknowledgment(self):
        ack_data = self.folder_socket.recv(3)
        
        if ack_data != b"ACK":
            print("Error: Acknowledgment not received.")
            return False
        
        return True

    def send_folder_thread(self, path):
        try:
            self.send_images(path)  
        except Exception as e:
            print(f"Error in send_folder_thread: {e}")
            
class UI_UX:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng hỗ trợ kiểm tra")
        self.root.resizable(False, False)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        if getattr(sys, 'frozen', False):
            self.current_directory = sys._MEIPASS
        else:
            self.current_directory = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(self.current_directory, 'app_img', 'logo_app.ico')
        self.root.iconbitmap(default=logo_path)
        
class Client_UI(UI_UX):
    def __init__(self, root, queue, path,IP,port):
        self.is_client_UI = False
        self.is_done = False
        self.photo_image = None
        self.back_ground = None
        self.queue = queue
        self.face_recognition_instance = None  # Initialize FaceRecognition instance
        self.path=path
        self.IP=IP
        self.port=port
        self.photo_image = None
        super().__init__(root)

    def img_config(self, img):
        if self.photo_image is None:
            img = cv2.resize(img, (self.root_width, self.root_height))
            self.photo_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            self.back_ground = tk.Label(self.frame, image=self.photo_image)
            self.back_ground.pack(fill=tk.BOTH, expand=True)
        else:
            img = cv2.resize(img, (self.root_width, self.root_height))
            new_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            self.back_ground.config(image=new_image)
            self.back_ground.image = new_image  # Keep a reference to avoid garbage collection

        self.root.update_idletasks()  # Update the window immediately


    def update_image_async(self):
        img = self.queue.get()
        if img is not None:
            self.img_config(img)
        self.root.after(self.update_interval, self.update_image_async)

    def client_main(self):
        name = self.name_user.get()
        num = self.user_num.get()
        class_ = self.user_class.get()
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.back_ground = tk.Label(self.frame)
        self.back_ground.pack(fill=tk.BOTH, expand=True)

        time_left = "00:45:00"

        tk.Label(self.frame, text=time_left, font=("Helvetica", 24)).place(x=450, y=10)
        tk.Label(self.frame, text=f"Tên: {name} Lớp: {class_} Số báo danh: {num}", font=("Helvetica", 15)).place(x=0, y=270)

        self.face_recognition_instance = FaceRecognition(self, self.queue, self.path, self.IP, self.port,name,num,class_,self.root_width,self.root_height)
        threading.Thread(target=self.face_recognition_instance.run_face_recognition).start()
        
    def create_ui(self):
        if not self.is_client_UI:
            self.Cx_position = self.screen_width * 2 // 3
            self.Cy_position = 0

            self.root_width = self.screen_width // 3
            self.root_height = self.screen_height // 2

            self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Cx_position}+{self.Cy_position}")

            self.top_frame = tk.Frame(self.root, bg="#FF69B4")
            self.top_frame.pack(side=tk.TOP, fill=tk.X)

            tk.Label(self.top_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black",
                     font=("Helvetica", 15, "bold"), bg="#99CCFF").pack(fill=tk.X)

            self.frame = tk.Frame(self.root, bg="#FFFAEC")
            self.frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.frame, text="Họ và tên:", height=2, bg="#FFFAEC", font=("Arial", 14)).pack(side=tk.TOP,anchor=tk.NW,padx=40)

            self.name_user = tk.Entry(self.frame, width=50)
            self.name_user.pack(side=tk.TOP,anchor=tk.NW,padx=40)
            self.name_user.config(highlightthickness=1, highlightbackground="black")

            tk.Label(self.frame, text="Số báo danh:", height=2, bg="#FFFAEC", font=("Arial", 14)).pack(side=tk.TOP,anchor=tk.NW,padx=40)

            self.user_num = tk.Entry(self.frame, width=50)
            self.user_num.pack(side=tk.TOP,anchor=tk.NW,padx=40)
            self.user_num.config(highlightthickness=1, highlightbackground="black")

            tk.Label(self.frame, text="Lớp:", height=2, bg="#FFFAEC", font=("Arial", 14)).pack(side=tk.TOP,anchor=tk.NW,padx=40)

            self.user_class = tk.Entry(self.frame, width=50)
            self.user_class.pack(side=tk.TOP,anchor=tk.NW,padx=40)
            self.user_class.config(highlightthickness=1, highlightbackground="black")

            self.login_button = tk.Button(self.frame, text="Hoàn tất", width=10, height=1, command=self.client_main,
                                          bg="#3366CC", font=("Arial", 15, "bold"))
            self.login_button.pack(side=tk.TOP,padx=40,pady=20)
            self.is_client_UI = True

        else:
            img = self.queue.get()
            if img is not None:
                self.root.after(50, self.update_image_async)

class FaceRecognition:
    def __init__(self, client_ui, queue, path, IP, port, name, num, class_,w,h):
        self.client_ui = client_ui
        self.cap = cv2.VideoCapture(0)
        self.warning_count = 1
        self.recognition = False
        self.x_border = self.y_border = 1e6
        self.x1_border = self.y1_border = 0
        if getattr(sys, 'frozen', False):
            self.current_directory = sys._MEIPASS
        else:
            self.current_directory = os.path.dirname(os.path.abspath(__file__))
        face_cascade_path = os.path.join(self.current_directory, 'Model', 'haarcascade_frontalface_alt.xml')
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
        nose_cascade_path = os.path.join(self.current_directory, 'Model', 'haarcascade_mcs_nose.xml')
        self.nose_cascade = cv2.CascadeClassifier(nose_cascade_path)
        self.current_folder_path = None
        self.set_camera_properties(w, h)
        self.queue = queue
        self.path = path
        self.IP = IP
        self.port = port
        self.name=name
        self.num=num
        self.class_=class_
        
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

    def send_folder(self,first_face,frame,client):
        if self.recognition:
            distance = abs(self.xmd_face - self.xmd_nose)

            if distance > 5 or first_face is None:
                self.put_text_on_frame(frame, 'Warning!!', 3)

                time_now = time.strftime("(%d-%m-%Y) (%H-%M-%S)", time.localtime())

                if not self.current_folder_path:
                    self.current_folder_path = os.path.join(self.path, f'Warning_{self.warning_count}')
                    self.create_folder(self.current_folder_path)

                    if os.path.exists(os.path.join(self.path, f'Warning_{self.warning_count - 1}')):
                        send_thread = threading.Thread(target=client.send_images,
                                                       args=(
                                                       os.path.join(self.path, f'Warning_{self.warning_count - 1}'),
                                                       f'Warning_{self.warning_count - 1}'), )

                        send_thread.start()
                        print(f'Sended Warning_{self.warning_count - 1}')

                    self.warning_count += 1

                self.take_photos(frame, time_now, self.current_folder_path)

            else:
                # Prepare for the next folder
                self.current_folder_path = None  # Reset to None
        else:
            if cv2.waitKey(25) & 0xFF == ord('q'):
                    if self.warning_count > 1:
                        send_thread = threading.Thread(target=client.send_images,
                                                       args=(
                                                           os.path.join(self.path, f'Warning_{self.warning_count - 1}'),
                                                           f'Warning_{self.warning_count - 1}'), )
                        send_thread.start()
                
    def run_face_recognition(self):
        try:
            client = Client()
            client.connect_server(self.IP, self.port)
            print("Connect successfully")
            client.client_type()
            print("Sending type successfully")
            client.send_info_video(self.name,self.class_)
            print("Sending info video successfully")
            client.send_info_folder(self.name,self.num,self.class_)
            print("Sending info folder successfully")
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Unable to read frame from the camera.")
                    break

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
                    self.xmd_face = round(x_face + w_face / 2)

                    x_nose, y_nose, w_nose, h_nose = first_nose
                    self.xmd_nose, ymd_nose = x_nose + w_nose // 2, y_nose + h_nose // 2

                    self.x_border = round(min((size[1] - w_face) / 2 + 10, self.x_border))
                    self.y_border = round(min((size[0] - h_face) / 2 + 10, self.y_border))
                    self.x1_border = round(max((size[1] + w_face) / 2 + 10, self.x1_border))
                    self.y1_border = round(max((size[0] + h_face) / 2 + 10, self.y1_border))

                    if not (self.x_border < x_face and self.y_border < y_face and
                            self.x1_border > x1_face and self.y1_border > y1_face):

                        cv2.rectangle(frame, (self.x_border, self.y_border), (self.x1_border, self.y1_border),
                                      (0, 0, 255), 1)
                        cv2.rectangle(frame, (x_nose, y_nose), (x_nose + w_nose, y_nose + h_nose), (255, 0, 0), 1)
                        cv2.rectangle(frame, (x_face, y_face), (x1_face, y1_face), (0, 255, 0), 1)

                        self.put_text_on_frame(frame, 'Please move your face into frame!', 1)
                
                self.client_ui.img_config(frame)
                              
                #threading.Thread(target=client.video_loop, args=(frame,)).start()
                #time.sleep(1)
                threading.Thread(target=self.send_folder, args=(first_face,frame,client,)).start()
            
                threading.Event().wait(0.1)                

            # Release the video capture object
            self.cap.release()

            # Closes all the frames
            cv2.destroyAllWindows()

            client.disconnect_server()

        except Exception as e:
            print(f"Error when trying to open camera: {e}")
            input("Press any key to quit")
            exit()

def run_gui_cl(queue,path,IP,port):
    root = tk.Tk()
    app = Client_UI(root, queue,path,IP,port)
    app.create_ui()
    root.mainloop()
