# Image AI Prediction Python Project

This project leverages computer vision, machine learning, and a graphical user interface (GUI) to perform real-time video frame analysis and predictions using a trained AI model. The project uses TensorFlow/Keras for training and making predictions, OpenCV for video capture, and tkinter for the GUI.

## Project Structure

- **`base.py`**:  
  This file is responsible for setting up a tkinter-based GUI for video display. It uses OpenCV to capture video from a camera source and creates a canvas where video frames are displayed.

- **`predict.py`**:  
  The core of the real-time prediction functionality. This script loads a pre-trained AI model using TensorFlow/Keras, processes video frames in real-time, and predicts class labels for the captured frames. The predictions are displayed in the GUI created using tkinter.

- **`snapshot.py`**:  
  Another GUI-driven script that captures live video frames. It likely includes functionality to take snapshots from the video stream and save or process them further.

- **`train.py`**:  
  The model training script. This script is responsible for setting up and training a machine learning model using the MobileNetV3Small architecture. The script includes data preprocessing, model building, and training steps.

## Prerequisites

To run this project, you will need the following libraries:

- `tensorflow`
- `opencv-python`
- `pillow` (PIL)
- `tkinter`
- `numpy`
