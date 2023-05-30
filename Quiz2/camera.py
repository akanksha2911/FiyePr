
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from datetime import datetime


#face_detection_videocam = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
faceDetect=cv2.CascadeClassifier(r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\home\\haarcascade_frontalface_default.xml')
class VideoCamera(object):
        
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
              
              ret,frame=self.video.read()
              ret,jpg=cv2.imencode('.jpg',frame)
              return jpg.tobytes()
             
		

		


	