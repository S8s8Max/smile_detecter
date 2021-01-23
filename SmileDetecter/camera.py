import sys
import os
import cv2
import datetime
import time

sys.path.append(os.path.abspath(".."))
from Components import face_detecter
from Components import smile_detecter



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
camera = cv2.VideoCapture(camera_id)

if not camera.isOpened():
    sys.exit()

while True:
    ret, frame = camera.read()

    # -----------------  Process images here. ---------------- #
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = frame[y:y + h, x:x + w]
        face_gray = gray[y:y + h, x:x + w]

        smiles = smile_cascade.detectMultiScale(face_gray, 1.8, 20)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(face, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

            # - Definition of SMILE - #
            # You are smile when the aspect ratio is higher than 2.0.
            smile_value = abs(abs(sw - sx) / abs(sy - sh))
            if smile_value > 2.0 and smile_value < 10:
                print(smile_value, "You are Smily!!")

            # store today's data to "today.csv"
            with open(os.path.dirname(os.path.abspath(__file__)) + "/Data/today.csv", "a") as f:
                now = datetime.datetime.now()
                now = now.strftime("%Y/%m/%d %H:%M:%S")
                f.write(f"{now},{smile_value}\n")
                time.sleep(1)

    # ----------------- End of Image Processing ----------------- #

    cv2.imshow(window_name, frame)
    key = cv2.waitKey(delay)
    if key == 27: # Escape by pressing ESC key
        break

camera.release()
cv2.destroyWindow(window_name)
