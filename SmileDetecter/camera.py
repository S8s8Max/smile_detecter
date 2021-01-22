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

##### Detect Face #####
face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)


##### MAIN #####
camera = cv2.VideoCapture(camera_id)

if not camera.isOpened():
    sys.exit()

while True:
    ret, img = camera.read()

    # -----  Process images here. ----- #
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = img[y: y + h, x: x + w]
        face_gray = gray[y: y + h, x: x + w]
    # --------------------------------- #

    cv2.imshow(window_name, img)
    key = cv2.waitKey(0)
    if key == 27: # ESC key
        break

camera.release()
cv2.destroyWindow(window_name)
