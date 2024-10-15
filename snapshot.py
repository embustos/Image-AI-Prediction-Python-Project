import os 
import cv2
import time 
import tkinter as tk 
from tkinter import messagebox 
from PIL import Image, ImageTk 

VIDEO_WIDTH = 1280 
VIDEO_HEIGHT = 720

class App:
    def __init__(self, window, window_title, video_source=0):
        self.photo = None 
        self.window = window 
        self.window.title(window_title) 
        self.video_source = video_source 

        self.vid = cv2.VideoCapture(video_source)

        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

        self.canvas = tk.Canvas(window, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
        self.canvas.pack()

        self.class_name_label = tk.Label(window, text="Class name(folder name):")  
        self.class_name_label.pack(side=tk.LEFT) 
        
        self.class_name_entry = tk.Entry(window, width=50) 
        self.class_name_entry.insert(0, "sample") 
        self.class_name_entry.pack(side=tk.LEFT, expand=True) 

        self.dialog = None 
        self.snapshot_count = 0
        self.snapshot_mode = False
        
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.toggle_snapshot) 
        self.btn_snapshot.pack(side=tk.RIGHT, pady=10, expand=True) 

        self.update() 
        self.window.mainloop()

    def create_dialog(self):
        dialog = tk.Toplevel(self.window) 
        dialog.geometry("300x100") 
        dialog.title("Dialog - capture 0 images.") 
        tk.Label(dialog, text="Capturing...").pack(pady=20) 
        tk.Button(dialog, text="Close", command=self.toggle_snapshot).pack() 
        self.dialog = dialog 

    def toggle_snapshot(self):
        self.snapshot_mode = not self.snapshot_mode 
        if self.snapshot_mode:
            self.btn_snapshot.config(text="Stop") 
            self.class_name_entry.config(state=tk.DISABLED) 
            self.create_dialog() 
            self.snapshot() 
        else:
            self.dialog.destroy() 
            self.dialog = None
            self.snapshot_count = 0 
            self.btn_snapshot.config(text="Snapshot") 
            self.class_name_entry.config(state=tk.NORMAL) 

    def snapshot(self): 
        if self.snapshot_mode:
            ret, frame = self.vid.read() 
            folder_name = os.path.join("data", self.class_name_entry.get()) 
            if folder_name == "":
                messagebox.showerror("Error", "Please input class name(folder name)!")
                return

            if not os.path.exists(folder_name): 
                os.mkdir(folder_name) 

            if ret: 
                filename = "frame-" + str(time.time()) + ".png" 
                cv2.imwrite(os.path.join(folder_name, filename), frame) 
                self.snapshot_count += 1
                if self.dialog is not None: 
                    self.dialog.title(f"Dialog - capture {self.snapshot_count} images.")

            self.window.after(100, self.snapshot) 

    def update(self):
        ret, frame = self.vid.read() 
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(15, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

root = tk.Tk() 

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - VIDEO_WIDTH) / 2
y = (screen_height - VIDEO_HEIGHT) / 2

root.geometry("%dx%d+%d+%d" % (VIDEO_WIDTH, VIDEO_HEIGHT + 100, x, y))

app = App(root, "Capture Image")
