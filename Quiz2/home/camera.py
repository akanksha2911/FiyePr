import cv2
import face_recognition
from training import encodeListKnown,personNames
import numpy as np
from datetime import datetime

faceDetect=cv2.CascadeClassifier(r'C:\Users\hpw\Desktop\akanksha1\Quiz2\home\haarcascade_frontalface_default.xml')

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)          #accessing front camera of laptop
    def __del__(self):
        self.video.release()         
    def get_frame(self):                                      #reading images from the camera
        ret,frame=self.video.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)                  
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):                #decoding the encoded images
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:                                        
                name = personNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)                            #adding rectangle boxes around face
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                #with open('Attendance.csv', 'r+') as f:   #adding name and date and time to attendance.csv file after recognization
                #    myDataList = f.readlines()
                #    nameList = []
                #    for line in myDataList:
                #        entry = line.split(',')
                #        nameList.append(entry[0])
                #    if name not in nameList:
                #        now = datetime.now()
                #        dtString = now.strftime('%H:%M:%S')
                #        f.writelines(f'\n{name},{dtString}')
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()