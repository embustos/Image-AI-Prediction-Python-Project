import os
import json
import tensorflow as tf
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

with open(os.path.join("models", "class_names.json"), "r") as f:
    class_names = json.load(f)

model = tf.keras.models.load_model(os.path.join("models", "my_model.h5"))
input_width, input_height = 244, 244

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - VIDEO_WIDTH) / 2
y = (screen_height - VIDEO_HEIGHT) / 2
window.geometry("%dx%d+%d+%d" % (VIDEO_WIDTH, VIDEO_HEIGHT + 50, x, y))
window.title("Camera with TensorFlow Prediction")

label = tk.Label(window)
label.pack()

def close():
    cap.release()
    window.quit()
    window.destroy()

button = tk.Button(window, text="Exit", width=20, pady=5, command=close)
button.pack()

cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        processed_frame = cv2.resize(frame, (input_width, input_height))
        processed_frame = np.expand_dims(processed_frame, axis=0)

        prediction = model.predict(processed_frame)
        print(prediction)

        percentage = np.max(prediction, axis=1)[0] * 100
        prediction_text = f"Prediction: {class_names[np.argmax(prediction, axis=1)[0]]}, {percentage:.2f}%"

        cv2.putText(frame, prediction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        display_frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))

        cv2image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        label.imgtk = imgtk
        label.configure(image=imgtk)

    window.after(20, update_frame)


update_frame()
window.mainloop()
