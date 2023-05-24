import numpy as np
from keras.preprocessing import image
import tensorflow as tf
import pickle
from tensorflow import keras

model = keras.models.load_model('classifier_model.h5')
# Load the ResultMap
with open('ResultsMap.pkl', 'rb') as file:
    ResultMap = pickle.load(file)

ImagePath='check.jpg' #testing image
test_image=tf.keras.utils.load_img(ImagePath,target_size=(64, 64))
test_image=tf.keras.utils.img_to_array(test_image)

test_image=np.expand_dims(test_image,axis=0)
result=model.predict(test_image,verbose=0)
#print(training_set.class_indices)

print('####'*10)
print('Prediction is: ',ResultMap[np.argmax(result)])