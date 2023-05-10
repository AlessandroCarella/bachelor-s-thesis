
from randomForestClassifier import getRandomForestClassifier


import cv2
import tkinter as tk

import tkinter as tk

def on_button_click(button_label, root):
    root._button_clicked = button_label # define _button_clicked attribute
    root.quit() # stop the mainloop

def create_buttons(root):
    button1 = tk.Button(root, text="Button 1", command=lambda:on_button_click(1, root))
    button2 = tk.Button(root, text="Button 2", command=lambda:on_button_click(2, root))
    button3 = tk.Button(root, text="Button 3", command=lambda:on_button_click(3, root))
    button4 = tk.Button(root, text="Button 4", command=lambda:on_button_click(4, root))

    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()

def pickClassifier(nTentative=0):
    root = tk.Tk()
    root.title("Button Example")

    create_buttons(root)

    root._button_clicked = None # initialize _button_clicked attribute

    root.mainloop() # start the mainloop

    pickedClassifier = root._button_clicked
    root.destroy() # destroy the root window

    if pickedClassifier == 1:
        return "ciao"#getRandomForestClassifier()
    elif pickedClassifier == 2:
        # do something for button 2
        pass
    else:
        return pickClassifier(nTentative+1)


    
print (pickClassifier ())