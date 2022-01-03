''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc  
Original Ref : https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/01_face_dataset.py   
Developed by Piyali Bhunia @3rd jan 2022  
'''

import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

font = cv2.FONT_HERSHEY_SIMPLEX

# Face detector using haarcascade classifier
# more such classifiers are present in - https://github.com/opencv/opencv/tree/master/data/haarcascades
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# for each new person, enter new numeric user id
face_id = input("Enter user id : ")
print("Initializing face capture, Look at the camera and please wait")

count = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        count += 1

        cv2.imwrite("dataset/user." + str(face_id) + "." + str(count) + ".jpg", gray[y:y+h, x:x+w])
        cv2.putText(img, str(count) + " Taken", (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.imshow('image', img)
        cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
        

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 50:
        break

print("Exiting Program")
cam.release()
cv2.destroyAllWindows()