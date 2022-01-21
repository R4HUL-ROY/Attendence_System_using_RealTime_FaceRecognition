import os
import numpy as np
import cv2
from tkinter import *
import tkinter.filedialog

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def collect_face():
    cam = cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)

    font = cv2.FONT_HERSHEY_SIMPLEX

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
        elif count >= 200:
            break

    print("Exiting Program")
    cam.release()
    cv2.destroyAllWindows()


def save_frame_from_video(video_path):
    user_id = input("Enter your id : ")
    print("Processing ... Please wait ...")
    cap = cv2.VideoCapture(video_path)
    idx = 1

    while True:
        ret, frame = cap.read()
        if ret == False:
            cap.release()
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.imwrite(f"dataset/user."+ str(user_id)+"."+str(idx)+".jpg", gray[y:y+h, x:x+w])
            idx += 1
            
if __name__ == "__main__":
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    print("1. Open camera & Capture Face data now")
    print("2. Already have a video")
    choice = int(input("Enter your choice : "))

    if choice == 1:
        collect_face()
    elif choice == 2:
        print("Please Browse your Video file...\n")
        filepath = tkinter.filedialog.askopenfilename()
        save_frame_from_video(filepath)