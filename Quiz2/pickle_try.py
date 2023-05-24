import numpy as np
from keras.preprocessing import image
import tensorflow as tf
import pickle
from tensorflow import keras
import os

model = keras.models.load_model('Quiz2\classifier_model.h5')
# Load the ResultMap
with open('Quiz2\ResultsMap.pkl', 'rb') as file:
    ResultMap = pickle.load(file)

ImagePath=r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\media\\captured_image.jpg' 
test_image=tf.keras.utils.load_img(ImagePath,target_size=(64, 64))
test_image=tf.keras.utils.img_to_array(test_image)

test_image=np.expand_dims(test_image,axis=0)
result=model.predict(test_image,verbose=0)
#print(training_set.class_indices)

print('####'*10)
print('Prediction is: ',ResultMap[np.argmax(result)])