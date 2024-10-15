import cv2 
import tkinter as tk 
from PIL import Image, ImageTk 

class App:
    def __init__(self, window, window_title, video_source=0):
        self.photo = None 
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.update()
        self.window.mainloop()

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
app = App(root, "Teachable Machine - Image Classification")
