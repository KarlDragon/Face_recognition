import os
import cv2
import time
import socket
import struct
import threading
import numpy as np

class Server:
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
