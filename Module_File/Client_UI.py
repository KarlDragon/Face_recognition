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
        self.root.iconbitmap(default=r"C:\C++\Homeworks\project\Module_File\app_img\logo_app.ico")

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
        super().__init__(root)

    def img_config(self, img):
        if self.back_ground:
            self.photo_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            self.back_ground.configure(image=self.photo_image)

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

        # Instantiate FaceRecognition only after the button is clicked
        self.face_recognition_instance = FaceRecognition(self, self.queue, self.path, self.IP, self.port)
        threading.Thread(target=self.face_recognition_instance.run_face_recognition).start()

    def create_ui(self):
        if not self.is_client_UI:
            self.Cx_position = self.screen_width * 2 // 3
            self.Cy_position = 0

            self.root_width = self.screen_width // 3
            self.root_height = self.screen_height // 3

            self.root.geometry(f"{self.root_width}x{self.root_height}+{self.Cx_position}+{self.Cy_position}")

            self.top_frame = tk.Frame(self.root, bg="#FF69B4")
            self.top_frame.pack(side=tk.TOP, fill=tk.X)

            tk.Label(self.top_frame, text="Trung học phổ thông Ba Gia", height=2, fg="black",
                     font=("Helvetica", 15, "bold"), bg="#99CCFF").pack(fill=tk.X)

            self.frame = tk.Frame(self.root, bg="#FFFAEC")
            self.frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.frame, text="Họ và tên:", height=2, bg="#FFFAEC", font=("Arial", 14)).place(x=50, y=0)

            self.name_user = tk.Entry(self.frame, width=50)
            self.name_user.place(x=50, y=self.root_height * 1 // 7 - 10)
            self.name_user.config(highlightthickness=1, highlightbackground="black")

            tk.Label(self.frame, text="Số báo danh:", height=2, bg="#FFFAEC", font=("Arial", 14)).place(x=50, y=120)

            self.user_num = tk.Entry(self.frame, width=50)
            self.user_num.place(x=50, y=160)
            self.user_num.config(highlightthickness=1, highlightbackground="black")

            tk.Label(self.frame, text="Lớp:", height=1, bg="#FFFAEC", font=("Arial", 14)).place(x=50, y=70)

            self.user_class = tk.Entry(self.frame, width=50)
            self.user_class.border_radius = 360
            self.user_class.place(x=50, y=100)
            self.user_class.config(highlightthickness=1, highlightbackground="black")

            self.login_button = tk.Button(self.frame, text="Hoàn tất", width=10, height=1, command=self.client_main,
                                          bg="#3366CC", font=("Arial", 15, "bold"))
            self.login_button.place(x=225, y=self.root_height * 5 // 7 - 20)
            self.is_client_UI = True

        else:
            img = self.queue.get()
            if img is not None:
                self.img_config(img)

class FaceRecognition:
    def __init__(self, client_ui, queue, path, IP, port):
        self.client_ui = client_ui
        self.cap = cv2.VideoCapture(0)
        self.warning_count = 1
        self.recognition = False
        self.x_border = self.y_border = 1e6
        self.x1_border = self.y1_border = 0
        self.face_cascade = cv2.CascadeClassifier(
            r'C:\C++\Homeworks\project\Module_File\Model\haarcascade_frontalface_alt.xml')
        self.nose_cascade = cv2.CascadeClassifier(r'C:\C++\Homeworks\project\Module_File\Model\haarcascade_mcs_nose.xml')
        self.current_folder_path = None
        self.set_camera_properties(1, 1)
        self.queue = queue
        self.path = path
        self.IP = IP
        self.port = port

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

    def run_face_recognition(self):
        try:
            client = Client()
            client.connect_server(self.IP, self.port)
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
                            self.current_folder_path = os.path.join(self.path, f'Warning_{self.warning_count}')
                            self.create_folder(self.current_folder_path)

                            if os.path.exists(os.path.join(self.path, f'Warning_{self.warning_count - 1}')):
                                send_thread = threading.Thread(target=client.send_images,
                                                               args=(
                                                               os.path.join(self.path, f'Warning_{self.warning_count - 1}'),
                                                               f'Warning_{self.warning_count - 1}'), )

                                send_thread.start()

                            self.warning_count += 1

                        self.take_photos(frame, time_now, self.current_folder_path)

                    else:
                        # Prepare for the next folder
                        self.current_folder_path = None  # Reset to None

                self.client_ui.img_config(frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    if self.warning_count > 1:
                        send_thread = threading.Thread(target=client.send_images,
                                                       args=(
                                                           os.path.join(self.path, f'Warning_{self.warning_count - 1}'),
                                                           f'Warning_{self.warning_count - 1}'), )
                        send_thread.start()
                    break

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


