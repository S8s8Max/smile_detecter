import sys
import os
import cv2
import datetime
import time
import PySimpleGUI as sg
import tkinter as Tk
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageFont, ImageDraw, Image

sys.path.append(os.path.abspath(".."))
from Data import cron
from Data import summaryData


###### GUI CONST ######
sg.theme("DarkTeal2")
frame1 = sg.Frame(layout=[[sg.Image(filename="", key="_IMAGE_")]],
                            title="Smile Detecter",
                            title_color="white",
                            font=("Courier", 20),
                            size=(900, 600),
                            relief=sg.RELIEF_SUNKEN,
                            element_justification="left")

layout = [
    [frame1],
    [sg.Text("Recording Switch", size=(20, 3), font="Courier 20")],
    [sg.Button("OFF", size=(10,2), font="Courier 14", key="_CAMERA_"),
     sg.Text("", size=(20,3), font="Courier 14", key="_SMILE_"),
     sg.Submit("Quit", size=(10,2), font="Courier 14"),]
]
win = sg.Window("Smile Detecter 😃", layout,
                                    location=(30,30),
                                    alpha_channel=1.0,
                                    no_titlebar=False,
                                    grab_anywhere=False,
                                    resizable=True,
                                    )


##### CONST #####
camera_id = 0
delay = 1
window_name = "Smile Detecter😃"

##### Detect Face( and SMILE ) #####
face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
smile_cascade_path = cv2.data.haarcascades + "haarcascade_smile.xml"

face_cascade = cv2.CascadeClassifier(face_cascade_path)
smile_cascade = cv2.CascadeClassifier(smile_cascade_path)

##### MAIN #####
# initialize the file which will be added data.
with open(os.path.dirname(os.path.abspath(__file__)) + "/Data/today.csv", "w") as f:
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d %H:%M:%S")
    f.write(f"{now},2.0\n")

camera = cv2.VideoCapture(camera_id)
camera.set(4, 1080)

if not camera.isOpened():
    sys.exit()

while True:
    event, values = win.read(timeout=1)
    if event in (None, "Quit"):
        break

    ret, frame = camera.read()

    image = frame[90:990, 510:1410]
    image_ = cv2.resize(image, (550,550), cv2.INTER_LANCZOS4)


    # -----------------  Process images here. ---------------- #
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = image[y:y + h, x:x + w]
        face_gray = gray[y:y + h, x:x + w]

        smiles = smile_cascade.detectMultiScale(face_gray, 1.8, 20)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(face, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

            # - Definition of SMILE - #
            # You are smile when the aspect ratio is higher than 2.0.
            smile_value = abs(abs(sw - sx) / abs(sh - sy))

            # store today's data to "today.csv"
            # if the data(date) already exists, won't store it.
            with open(os.path.dirname(os.path.abspath(__file__)) + "/Data/today.csv", "r+") as f:
                now = datetime.datetime.now()
                now = now.strftime("%Y/%m/%d %H:%M:%S")
                lines = f.readlines()
                last_d, last_v = lines[-1].split(",")
                if str(now) == last_d:
                    if smile_value >= 1.6 and smile_value < 10:
                        f.write(f"{now},{smile_value}\n")
                    pass
                else:
                    if smile_value >= 2 and smile_value < 10:
                        print("Nice Smile", smile_value)
                    f.write(f"{now},{smile_value}\n")

    # ----------------- End of Image Processing ----------------- #

    imgbytes = cv2.imencode('.png', image)[1].tobytes()
    win["_IMAGE_"].update(data=imgbytes)

win.close()
