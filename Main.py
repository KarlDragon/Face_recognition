import cv2
import os
import time
import socket
import struct
import threading
import numpy as np

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_server(self, IP, port):
        self.client_socket.connect((IP, port))

    def disconnect_server(self):
        self.client_socket.close()

    def send_images(self, folder_path):
        for filename in os.listdir(folder_path):
            
            conn.sendall(folder_path.encode('utf-8'))
            
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

class FaceRecognition:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.warning_count = 1
        self.recognition = False
        self.x_border = self.y_border = 1e6
        self.x1_border = self.y1_border = 0
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self.current_folder_path = None  


        self.set_camera_properties(1, 1)

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

                    distance = abs(xmd_face - xmd_nose)

                if distance > 4 or first_face is None:
                    self.put_text_on_frame(frame, 'Warning!!', 3)

                    time_now = time.strftime("(%d-%m-%Y) (%H-%M-%S)", time.localtime())

                    if not self.current_folder_path:
                        self.current_folder_path = os.path.join(path, f'Warning_{self.warning_count}')
                        self.create_folder(self.current_folder_path)

                        if os.path.exists(os.path.join(path, f'Warning_{self.warning_count - 1}')):
                            send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count - 1}',),))

                            send_thread.start()

                        self.warning_count += 1

                    self.take_photos(frame, time_now, self.current_folder_path)

                else:
                    # Prepare for the next folder
                    self.current_folder_path = None  # Reset to None

                cv2.imshow('Frame', frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count}',),))
                    send_thread.start()
                    break
            
            # Release the video capture object
            self.cap.release()

            # Closes all the frames
            cv2.destroyAllWindows()

            client.disconnect_server()  # Corrected method name

        except Exception as e:
            print(f"Error when trying to open camera: {e}")
            input("Press any key to quit")
            exit()
            

    
    
if __name__ == "__main__":
    
    mode=input("Please choose your mode (sv,cl): ")
    path=input("Please type your path: ")
    IP=input("Please type sever IP: ")
    port=int(input("Please type sever port: "))

    if mode=='cl':
        face_recognition = FaceRecognition()
        face_recognition.run_face_recognition(path, IP, port)
             
    elif mode=='sv':
        client_num = int(input("Please type the amount of clients: "))

        sever = Sever()
        sever.start_server(path,IP,port,client_num)
