import os
import threading
import tkinter as tk
from Module_File import Server_UI, Client_UI, First_time_UI, FaceRecognition

class AppManager:
    def __init__(self):
        self.is_txt = os.path.exists('information.txt')

    def run_feature(self, path, IP, port):
        feature = FaceRecognition.FaceRecognition()
        feature.run_face_recognition(path, IP, port)

    def run_client_ui(self):
        root = tk.Tk()
        app = Client_UI.Client_UI(root)
        app.Cl_UI()
        root.mainloop()

    def run_server_ui(self):
        app = Server_UI.Server_UI(2, 2)

    def run_first_time_ui(self):
        app = First_time_UI.First_time_UI()

    def start_threads(self, mode, path, IP, port):
        if mode == "Cl":
            thread_ui = threading.Thread(target=self.run_client_ui)
            thread_feature = threading.Thread(target=self.run_feature, args=(path, IP, port))

            thread_ui.start()
            thread_feature.start()

        elif mode == "Sv":
            thread_server = threading.Thread(target=self.run_server_ui)
            thread_server.start()

        else:
            thread_first_time_ui = threading.Thread(target=self.run_first_time_ui)
            thread_first_time_ui.start()

if __name__ == "__main__":
    app_manager = AppManager()

    if app_manager.is_txt:
        with open('information.txt', 'r') as f:
            mode = f.readline().replace('\n', '')
            path = f.readline().replace('\n', '')
            IP = f.readline().replace('\n', '')
            port = int(f.readline())

        app_manager.start_threads(mode, path, IP, port)
    else:
        app_manager.start_threads("", "", "", 0)
