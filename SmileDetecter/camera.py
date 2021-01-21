import sys
import os
import cv2

sys.path.append(os.path.abspath(".."))
from Components import face_detecter
from Components import smile_detecter

##### CONST #####
camera_id = 0
delay = 1
window_name = "Smile Detecter😃"


##### MAIN #####
camera = cv2.VideoCapture(camera_id)

if not camera.isOpened():
    sys.exit()

while True:
    ret, frame = camera.read()

    # -----  Process images here. ----- #
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (0, 0), 5)
    # --------------------------------- #

    cv2.imshow(window_name, blur)
    if cv2.waitKey(delay) & 0xFF == ord("q"):
        break

cv2.destroyWindow(window_name)
