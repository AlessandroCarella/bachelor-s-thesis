import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
from os.path import join, isfile, abspath, dirname
import os
from feat import Detector
import torch
import numpy as np
import pickle

from pickClassifier import pickClassifier, predictProba, getModelPredictionText

def buildNewDetector (filePathDetector):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #device = "cpu"
    detector = Detector(
        face_model="retinaface",
        landmark_model="mobilefacenet",
        au_model="xgb",
        emotion_model="resmasknet",
        facepose_model="img2pose",
        device=device,
    )
    
    with open (filePathDetector, "wb") as f:
        pickle.dump (detector, f)

    print (detector.device)
    return detector

def getDetector ():
    filePathDetector = join(dirname(abspath(__file__)), "detector.pickle")
    if isfile (filePathDetector):
        with open (filePathDetector, "rb") as f:
            detector = pickle.load (f)
        if detector.device == "cuda" and not torch.cuda.is_available():
            detector = buildNewDetector (filePathDetector)
    else:
        detector = buildNewDetector (filePathDetector)

    return detector

def createRootWindow():
    # Define the GUI window
    root = tk.Tk()
    root.title("Stato d'animo detection")
    root.protocol("WM_DELETE_WINDOW", onClosing)
    return root

def createVideoStreamFrame(root):
    # Create a frame to hold the video stream
    frame = tk.Frame(root)
    frame.pack(side="left")
    return frame

def createCanvas(frame):
    # Create a canvas to display the video stream
    canvas = tk.Canvas(frame, width=640, height=480)
    canvas.pack()
    return canvas

def createTextFrame(root):
    # Create a frame to hold the text widget
    textFrame = tk.Frame(root)
    textFrame.pack(side="right")
    return textFrame

def createTextWidget(textFrame):
    # Create a text widget to display text
    textWidget = tk.Text(textFrame, width=50, height=20, state="normal", font=("TkDefaultFont", 16))
    textWidget.tag_configure("center", justify='center')
    textWidget.tag_add("center", "1.0", "end")
    textWidget.pack()
    return textWidget

def getGUI():
    root = createRootWindow()
    return (
        createCanvas(createVideoStreamFrame(root)), 
        createTextWidget(createTextFrame(root)), 
        root)

def getPyFeatAnalysis():
    detectImageOutput = detector.detect_image(imagePath)
    AUs = detectImageOutput.aus.loc[0]
    facePos = list(list(zip(*detectImageOutput.facebox.loc[0].items()))[1])
    return AUs, facePos

def onClosing():
    global windowClosed
    windowClosed = True
    root.quit()

# Define a function to update the video stream
def update(cap, canvas, textWidget, root, imagePath):
    global lastSaveTime, userChosenClassifier, windowClosed, bestClassesLastMinute, lastPredictionTime
    
    frame = readFrame(cap)
    if frame is not None:
        img = convertFrameToImage(frame)
        updateCanvas(canvas, img)
        
    saveFrame(frame, imagePath)
    lastSaveTime = time.time()
    
    AUs, facePos = getPyFeatAnalysis()
    
    timeDiff = time.time() - lastPredictionTime
    lastPredictionTime = time.time()
    predictionText, bestClassesLastMinute = getPredictionText(AUs, userChosenClassifier, timeDiff, bestClassesLastMinute)
    updateTextWidget(textWidget, predictionText)
    
    drawFaceRectangle(canvas, facePos)
    
    if not windowClosed:
        root.after(20, update, cap, canvas, textWidget, root, imagePath)
    else:
        releaseCapture(cap)
        closeWindows()
        removeImageIfExists(imagePath)
             
def readFrame(cap):
    ret, frame = cap.read()
    return frame if ret else None    

def convertFrameToImage(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    return img

def updateCanvas(canvas, img):
    canvas.create_image(0, 0, anchor="nw", image=img)
    canvas.image = img

def saveFrame(frame, imagePath):
    cv2.imwrite(imagePath, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

def getPredictionText(AUs, userChosenClassifier, timeDiff, bestClassesLastMinute):
    try:
        AUs2d = np.array(AUs).reshape(1, -1)
        prediction = predictProba(userChosenClassifier, userChosenClassifierObj, AUs2d)
        if prediction is not None:
            output, bestClassesLastMinute = getModelPredictionText (userChosenClassifier, prediction, timeDiff, bestClassesLastMinute)
            return output, bestClassesLastMinute
        else:
            return "\n\n\n\n\n\n\n\n\nErrore con il modello predittivo", bestClassesLastMinute
    except Exception as e:
        print (e)
        return "\n\n\n\n\n\n\n\n\nNessuna faccia rilevata", bestClassesLastMinute

def updateTextWidget(textWidget, text):
    textWidget.delete("1.0", tk.END)
    textWidget.insert("1.0", text)
    textWidget.tag_configure("center", justify='center')
    textWidget.tag_add("center", "1.0", "end")
    
def drawFaceRectangle(canvas, facePos):
    canvas.create_rectangle(
        facePos[0], 
        facePos[1], 
        facePos[0] + facePos[2], 
        facePos[1] + facePos[3], 
        outline='purple', width=2
    )
     
def releaseCapture(cap):
    cap.release()
    
def closeWindows():
    cv2.destroyAllWindows()
    
def removeImageIfExists(imagePath):
    if os.path.isfile(imagePath):
        os.remove(imagePath)

def initializeWebcam():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, 1.5)  # Adjust the exposure value (0.0 to 1.0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the width to 640 pixels
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the height to 480 pixels
    cap.set(cv2.CAP_PROP_FPS, 24)  # Set the frame rate to 15 fps
    return cap

def handleProgramClose():
    # Release the webcam when the program exits
    cap.release()
    cv2.destroyAllWindows()

    if isfile(imagePath):
        os.remove(imagePath)

if __name__ == '__main__':
    windowClosed = False

    canvas, textWidget, root = getGUI()
    cap = initializeWebcam()

    imagePath = join(dirname(abspath(__file__)), "tempImg.jpg")
    detector = getDetector()
    userChosenClassifier, userChosenClassifierObj = pickClassifier()
    bestClassesLastMinute = {}
    lastPredictionTime = time.time()

    # Start the update loop
    update(cap, canvas, textWidget, root, imagePath)
    # Start the GUI main loop
    root.mainloop()

    handleProgramClose()
