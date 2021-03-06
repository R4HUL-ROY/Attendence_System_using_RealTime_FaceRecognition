import cv2
import numpy as np
import os 
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

def mark_attendence(name):
    with open('attendence_sheet.csv','r+') as f:

        #include all names into present_list whose name already in csv file
        csv = f.readlines()
        present_list = []
        for this_name in csv:
            entry = this_name.split(',')
            present_list.append(entry[0])

        #write to csv when the name is a new name which is not in the csv
        if name not in present_list:   
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f"\n{name},{dtstring}")

id = 0
# names related to ids:
names = ['None', 'Dipprokash Sardar','Anusha Sil', 'Sujata De','None','Ranjita Chakraborty','Manisha Ghosh','Anupam Jana','Masidur Rahaman','Shiuli Dey','Paromita Chel','Soumen Khara','Arnab Mondal',
'Mansur Alam','Subharanjan Das','Sumit Paul','Subhajit Das','Arit Biswas','Susmita Dey','Piyali Bhunia','Sudip Roy','Subham Pradhan','None','Sumit Das','Indrani Maity','Pradip Das','Arka Saha','Arnab Koley','Subrata Jana','Mouli Mondal','Sushma Tiwary','Debabrata Doloi','Rahul Roy','Hrikdhiman Dutta','Anupam Rakshit'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        
    if str(id) in names:  
        mark_attendence(str(id))
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()