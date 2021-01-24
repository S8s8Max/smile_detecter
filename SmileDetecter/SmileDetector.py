import sys
import os
import cv2
import datetime
import time
import PySimpleGUI as sg
import numpy as np
from matplotlib import pyplot as plt


###### GUI CONST ######
sg.theme("Black")
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 200
COLOR = "#d34545"

class Observer(object):
    def __init__(self, graph_elem, starting_count, color):
        self.graph_current_item = 0
        self.graph_elem = graph_elem    # type = sg.Graph
        self.prev_value = starting_count
        self.color = color
        self.line_list = []             #list of currently visible lines. used to delete old figures.

    def graph_percentage_abs(self, value):
        self.line_list.append(self.graph_elem.draw_line(
            (self.graph_current_item, 0),
            (self.graph_current_item, value),
            color=self.color))
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.move(-1,0)
            self.graph_elem.delete_figure(self.line_list[0])
            self.line_list = self.line_list[1:]
        else:
            self.graph_current_item += 1


def main():
    frame1 = sg.Frame(layout=[[sg.Image(filename="", key="_IMAGE_")]],
                                title="Smile Detector",
                                title_color="white",
                                font=("Courier", 50),
                                relief=sg.RELIEF_SUNKEN,
                                element_justification="left")
    Graph1 = sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT),
                                (0,0),
                                (GRAPH_WIDTH, 100),
                                background_color="black",
                                key="_GRAPH1_")
    layout = [
        [frame1, Graph1],
        [sg.Text("YOUR SMILE : ", size=(20,3), font="Courier 40",),
        sg.Text("", size=(20,3), font="Courier 40", key="_SMILE_")],
        [sg.Text("TODAY'S MAX : ", size=(20,3), font="Courier 40"),
         sg.Text("", size=(20,3), font="Courier 40", key="_MAX_SMILE_")],
        [sg.Button("Quit", size=(10,2), font="Courier 20", ),
         sg.Button("Report", size=(10,2), font="Courier 20", )]
    ]
    win = sg.Window("Smile Detector", layout,
                                        location=(30,30),
                                        alpha_channel=1.0,
                                        no_titlebar=False,
                                        grab_anywhere=False,
                                        resizable=True,
                                        use_default_focus=False,
                                        element_padding=(0,0),
                                        border_depth=0,
                                        margins=(1,1),
                                        pad=(1,1),
                                        finalize=True)
    graph = Observer(win["_GRAPH1_"], 0, COLOR)

    ##### CONST #####
    camera_id = 0
    delay = 1
    window_name = "Smile Detector"

    ##### Detect Face( and SMILE ) #####

    face_cascade = cv2.CascadeClassifier("/Users/kippeiwatanabe/Desktop/smile_detecter/SmileDetecter/Data/haarcascade_frontalface_default.xml")
    smile_cascade = cv2.CascadeClassifier("/Users/kippeiwatanabe/Desktop/smile_detecter/SmileDetecter/Data/smilecascade.xml")

    ##### MAIN #####
    # initialize the file which will be added data.
    #with open(os.path.dirname(os.path.abspath(__file__)) + "/Data/today.csv", "w") as f:
    #    now = datetime.datetime.now()
    #    now = now.strftime("%Y/%m/%d %H:%M:%S")
    #    f.write(f"{now},2.0\n")

    camera = cv2.VideoCapture(camera_id)
    camera.set(4, 1080)

    max_smile = 0
    stage = 0
    
    if not camera.isOpened():
        sys.exit()

    while True:
        event, values = win.read(timeout=1)
        if event in (None, "Quit"):
            break

        ret, frame = camera.read()

        image = frame[90:990, 0:-1]
        image_ = cv2.resize(image, (750,400), cv2.INTER_LANCZOS4)


        # -----------------  Process images here. ---------------- #
        gray = cv2.cvtColor(image_, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        smile_value = 0

        for (x, y, w, h) in faces:
            cv2.rectangle(image_, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = image_[y:y + h, x:x + w]
            face_gray = gray[y:y + h, x:x + w]

            smiles = smile_cascade.detectMultiScale(face_gray, 1.8, 20)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(face, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

                # - Definition of SMILE - #
                # You are smile when the aspect ratio is higher than 2.0.
                smile_value = abs(abs(sw - sx) / abs(sh - sy))
                # store today's data to "today.csv"
                # if the data(date) already exists, won't store it.
                """
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
                        f.write(f"{now},{smile_value}\n")
                """
        # ----------------- End of Image Processing ----------------- #

        imgbytes = cv2.imencode('.png', image_)[1].tobytes()
        win["_IMAGE_"].update(data=imgbytes)

        if smile_value > max_smile:
            max_smile = smile_value
            win["_MAX_SMILE_"].update(max_smile)
        win["_SMILE_"].update(str(smile_value))

        graph.graph_percentage_abs(smile_value * 40)

    win.close()

if __name__=="__main__":
    main()
