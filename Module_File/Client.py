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

