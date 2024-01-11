import tkinter as tk
from PIL import Image, ImageTk

def on_button_click():
    print("LOL")

# Create the main window
root = tk.Tk()
root.title("Image Button Example")
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

Rx_position = screen_width * 2 // 3
Ry_position = 0

root_width = screen_width // 3
root_height = screen_height // 3

root.geometry(f"{root_width}x{root_height}+{Rx_position}+{Ry_position}")

# Create a frame for the bottom row
bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

label = tk.Label(bottom_frame, text="THPT Ba Gia", height=2, fg="black", font="large_font", bg="yellow")
label.pack(fill=tk.X)

frame = tk.Frame(root, bg="blue")
frame.pack(fill=tk.BOTH, expand=True)

login_button = tk.Button(frame, text="Login", width=8)
login_button.place(x=root_width * 3 // 4, y=root_height * 5 // 7)

name_user = tk.Entry(frame)
name_user.place(x=0,y=root_height*1//7)

user_num = tk.Entry(frame)
user_num.place(x=0,y=root_height*2//7)

user_class = tk.Entry(frame)
user_class.place(x=root_width*7//12,y=root_height*1//7)

# Configure the weight of the row containing the login_button
frame.grid_rowconfigure(1, weight=1)

# Run the Tkinter event loop
root.mainloop()
