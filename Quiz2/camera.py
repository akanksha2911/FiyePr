
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from datetime import datetime
import face_recognition

#face_detection_videocam = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
faceDetect=cv2.CascadeClassifier(r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\home\\haarcascade_frontalface_default.xml')
class VideoCamera(object):
        
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
              
              #global matches,faceDis,faceLoc
              ret,frame=self.video.read()
              # faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
              # faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

              # facesCurrentFrame = face_recognition.face_locations(faces)                  
              # encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

            #   for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):                #decoding the encoded images
            #          matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            #          faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #          #print(faceDis)
            #   matchIndex = np.argmin(faceDis)

            #   if matches[matchIndex]:                                        
            #      name = personNames[matchIndex].upper()
                 
                       
            #      #print(name)
            #      y1, x2, y2, x1 = faceLoc
            #      y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            #      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)                            #adding rectangle boxes around face
            #      cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            #      cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                #  with open(r'C:\Users\hpw\Desktop\project with cnn\Attendance.csv', 'r+') as f:   #adding name and date and time to attendance.csv file after recognization
                #     myDataList = f.readlines()
                #     nameList = []
                #     for line in myDataList:
                #         entry = line.split(',')
                #         nameList.append(entry[0])
                #     if name not in nameList:
                #         now = datetime.now()
                #         dtString = now.strftime('%H:%M:%S')
                #         f.writelines(f'\n{name},{dtString}')
              ret,jpg=cv2.imencode('.jpg',frame)
              return jpg.tobytes()
              #return matchList
		# success, image = self.video.read()
		# # We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# # so we must encode it into JPEG in order to correctly display the
		# # video stream.

		# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		# for (x, y, w, h) in faces_detected:
		# 	cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		# frame_flip = cv2.flip(image,1)
		# ret, jpeg = cv2.imencode('.jpg', frame_flip)
		# return jpeg.tobytes()

		


	