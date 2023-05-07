import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
from os.path import join, isdir, isfile, abspath, dirname
import os
from feat import Detector
import torch
import threading
from randomForestClassifier import getRandomForestClassifier
import numpy as np

last_save_time = time.time()  # Declare the variable outside the function

def getDetector ():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return Detector(
        face_model="retinaface",
        landmark_model="mobilefacenet",
        au_model="xgb",
        emotion_model="resmasknet",
        facepose_model="img2pose",
        device=device,
    )

def getGUI():
    # Define the GUI window
    root = tk.Tk()
    root.title("Stato d'animo detection")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Create a frame to hold the video stream
    frame = tk.Frame(root)
    frame.pack(side="left")

    # Create a canvas to display the video stream
    canvas = tk.Canvas(frame, width=640, height=480)
    canvas.pack()

    # Create a frame to hold the text widget
    text_frame = tk.Frame(root)
    text_frame.pack(side="right")

    # Create a text widget to display text
    text_widget = tk.Text(text_frame, width=50, height=20, state="normal", font=("TkDefaultFont", 16))
    text_widget.tag_configure("center", justify='center')
    text_widget.tag_add("center", "1.0", "end")
    text_widget.pack()

    return canvas, text_widget, root

def getPyFeatAnalysis ():
    detectImageOutput = detector.detect_image (imagePath)
    AUs = detectImageOutput.aus.loc[0]
    facePos = list(list(zip(*detectImageOutput.facebox.loc[0].items()))[1])
    return AUs, facePos

def on_closing():
    global window_closed
    window_closed = True
    root.quit()

# Define a function to update the video stream
def update(cap, canvas, text_widget, root, imagePath):
    global last_save_time, randomForestClassifier, window_closed  # Use the global variable

    ret, frame = cap.read()
    if ret:
        # Convert the frame to a PIL image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        # Update the canvas with the new image
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.image = img

    # Save the current frame as an image
    cv2.imwrite(imagePath, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    last_save_time = time.time()  # Update the variable

    AUs, facePos = getPyFeatAnalysis ()
    AUs_2d = np.array(AUs).reshape(1, -1)

    try:    
        prediction = randomForestClassifier.predict_proba(AUs_2d)
        bestClass = ""
        max_prob = 0
        text = ""
        for i, label in enumerate(randomForestClassifier.classes_):
            prob = prediction[0][i]*100
            text += "{}: {:.2f}%\n".format(label, prob)
            if prob > max_prob:
                max_prob = prob
                bestClass = label
        text = "\n\n\n\n\nMood rilevato: " + bestClass + "\n\nCon i valori:\n" + text
    except Exception as e:
        text = "\n\n\n\n\n\n\n\n\nNessuna faccia rilevata"
    
    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", text)
    text_widget.tag_configure("center", justify='center')
    text_widget.tag_add("center", "1.0", "end")


    # Draw a rectangle around the face
    canvas.create_rectangle(facePos[0], facePos[1], facePos[0]+facePos[2], facePos[1]+facePos[3], outline='green', width=2)
    
    if not window_closed:
        # Schedule the update function to be called again in 20 milliseconds
        root.after(20, update, cap, canvas, text_widget, root, imagePath)
    else:
        cap.release()
        cv2.destroyAllWindows()
        if isfile(imagePath):
            os.remove(imagePath)

window_closed = False

imagePath = join(dirname(abspath(__file__)), "tempImg.jpg")
print (imagePath)

canvas, text_widget, root = getGUI()

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 1.5)  # Adjust the exposure value (0.0 to 1.0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the width to 640 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the height to 480 pixels
cap.set(cv2.CAP_PROP_FPS, 24)  # Set the frame rate to 15 fps

detector = getDetector()
randomForestClassifier = getRandomForestClassifier()

# Start the update loop
update(cap, canvas, text_widget, root, imagePath)

# Start the GUI main loop
root.mainloop()

# Release the webcam when the program exits
cap.release()
cv2.destroyAllWindows()

if isfile(imagePath):
    os.remove(imagePath)