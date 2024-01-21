import os
import threading
import tkinter as tk
from Module_File import Server_UI, Client_UI, First_time_UI
from queue import Queue

class AppManager:
    def __init__(self):
        self.is_txt = os.path.exists('information.txt')

    def run_client(self,path, IP, port):
        frame_queue = Queue()

        gui_thread = threading.Thread(target=Client_UI.run_gui, args=(frame_queue,path, IP, port,))
        gui_thread.start()

        gui_thread.join()

if __name__ == "__main__":
    
    app_manager = AppManager()

    if app_manager.is_txt:
        with open('information.txt', 'r') as f:
            mode = f.readline().replace('\n', '')
            path = f.readline().replace('\n', '')
            IP = f.readline().replace('\n', '')
            port = int(f.readline())
        if mode=="Cl":
            app_manager.run_client(path, IP, port)
    else:
        #app_manager.start_threads("", "", "", 0)
        pass
