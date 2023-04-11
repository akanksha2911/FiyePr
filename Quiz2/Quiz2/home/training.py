import cv2
import numpy as np
import face_recognition
import os

path = 'media\images'
images = []
personNames = []
myList = os.listdir(path)
print(myList)
for cu_img in myList:                                              #adding name to the recognized face
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)
    personNames.append(os.path.splitext(cu_img)[0])
print(personNames)


def faceEncodings(images):                #encoding the input face from camera
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = faceEncodings(images)
print('All Encodings Complete!!!')

#cap = cv2.VideoCapture(0)
