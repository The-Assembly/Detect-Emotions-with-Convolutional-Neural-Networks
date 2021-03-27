# -*- coding: utf-8 -*-
"""Emotion Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cMzRsuAfSInBfaq7_nPyhYcPh3TBK4yK

#Importing libraries
"""

import pandas as pd                       #reading, writing and manipulating the data (using tables)
import numpy as np                        #Library for linear algebra and some probabiltity (raw data)
import tensorflow as tf                       
from keras.models import Sequential       #To create the sequential layer

#from keras.layers.core import Flatten, Dense, Dropout     #To create the model
#from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D  #To create the model
from keras.preprocessing import image             #used for image classification
from keras.preprocessing.image import ImageDataGenerator  #used to expand the training dataset in order to improve the performance and ability of the model to generalize

from keras.layers import Dense, Conv2D, MaxPool2D , Flatten, Dropout
from keras.optimizers import SGD, Adam          #To use the optimizer
from keras.utils import np_utils  

#import cv2                                #CV (computer vision)
#from google.colab import files            #To be able to upload files

"""#Uploading Dataset

The Data set contains 48 X 48-pixel grayscale images of the face. There are seven categories **(0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral)** present in the data. The CSV file contains two columns that are emotion that contains numeric code from 0-6 and a pixel column that includes a string surrounded in quotes for each image.
"""

print('Upload the CSV file')
#uploaded = files.upload()
emotion_data = pd.read_csv('/content/drive/MyDrive/fer2013.csv')
print(emotion_data)

"""#Storing Dataset

We will create different lists for storing **the labels and the pixels** of both the **training and testing data**. We check the usuage colume in the csv file for each row if it is training then the pixels will be appended to the training array, but if its testing then the pixels will be appended to the testing array.
"""

#---------------------- Spliting the DataSet------------------------------------
X_train = []      #train pixels
y_train = []      #train labels
X_test = []       #test pixels
y_test = []       #test label
for index, row in emotion_data.iterrows():    #iterate on each row and store it
    k = row['pixels'].split(" ")       #list of pixels, each pixel is an element
    try:
      if row['Usage'] == 'Training':    
          X_train.append(np.array(k,'float32'))    #The desired data-type for the array is 
          y_train.append(row['emotion'])
      elif row['Usage'] == 'PublicTest':
          X_test.append(np.array(k,'float32'))
          y_test.append(row['emotion'])
    except:
      print(f"error occured at index :{index} and row:{row}")




print(X_test)
print(type(X_test))


print(y_train)
print(type(y_train))

"""

1.   Convert the arrays to numpy arrays so we can do several operations on it related to numpy library only like reshaping and dividing into categories
2.   Reshape the pixels arrays to be 48*48 array and each array has 1 element/pixel
3.   Convert the labels arrays into categorial ones, this function returns a matrix of binary values and have **rows numbers = the input vector dimensions** and have **columns numbers = the number of categories**  
        
        For example:


```
#Function
train_labels = to_categorical(train_labels, num_classes = 10)

#train_lables array before the function
array([[6],[9],[9]) 

#Labels after applying the function with 10 categories
[[0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 1]
 [0 0 0 0 0 0 0 0 0 1]]

```

"""

#--------------------Convert Lists to Numpy arrays------------------------------
X_train = np.array(X_train, 'float32')
y_train = np.array(y_train, 'float32')
X_test = np.array(X_test,'float32')
y_test = np.array(y_test,'float32')

#-----------------------Reshape Pixels arrays---------------------------------
#normalizing data between o and 1  
X_train -= np.mean(X_train, axis=0)  
X_train /= np.std(X_train, axis=0)  

X_test -= np.mean(X_test, axis=0)  
X_test /= np.std(X_test, axis=0) 

#reshape the numpy array to be passed to the model
X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)   
X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)

print(X_test.shape)
print(type(X_test))
print(X_train.shape)

#------------------Convert Labels array to categorial ones---------------------
#y_train= tf.keras.utils.to_categorical(y_train, num_classes=7)
#y_test = tf.keras.utils.to_categorical(y_test, num_classes=7)

y_train= np_utils.to_categorical(y_train, num_classes=7)
y_test = np_utils.to_categorical(y_test, num_classes=7)
print(y_train)
print(y_train.shape)
print(type(y_train))

"""#Build CNN model

We will be building a specific type of CNN model which is the VGG16 (Very Deep Convolutional Networks for Large-Scale Image Recognition) which is Convolutional Network for Classification and Detection.
The model will consist of initialization of the model followed by batch normalization layer and then different convents layers with ReLu as an activation function, max pool layers, and dropouts to do learning efficiently.
"""

#model1 = Sequential()

#model1.add(ZeroPadding2D((1,1),input_shape=(48,48,1)))
#model1.add(Convolution2D(64, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(64, 3, 3, activation='relu'))
#model1.add(MaxPooling2D(pool_size=(2,2), strides=(2,2),padding="same"))

#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(128, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(128, 3, 3, activation='relu'))
#model1.add(MaxPooling2D(pool_size=(2,2), strides=(2,2),padding="same"))

#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(256, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(256, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(256, 3, 3, activation='relu'))
#model1.add(MaxPooling2D(pool_size=(2,2), strides=(2,2),padding="same"))

#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(MaxPooling2D(pool_size=(2,2), strides=(2,2),padding="same"))


#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(ZeroPadding2D((1,1)))
#model1.add(Convolution2D(512, 3, 3, activation='relu'))
#model1.add(MaxPooling2D((2,2), strides=(2,2),padding="same"))

#model1.add(Flatten())
#model1.add(Dense(4096, activation='relu'))
#model1.add(Dropout(0.5))
#model1.add(Dense(4096, activation='relu'))
#model1.add(Dropout(0.5))
#model1.add(Dense(7, activation='softmax'))


#model1.summary()

model = Sequential()

model.add(Conv2D(input_shape=(X_train.shape[1:]),filters=64,kernel_size=(3,3),padding="same", activation="relu"))
model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))


model.add(Flatten())
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))


model.summary()

"""#Compile Model

We compile the model using Adams as optimizer,loss as categorical cross-entropy, and metrics as accuracy
"""

model.compile(optimizer=Adam(learning_rate=0.0001),loss='categorical_crossentropy',metrics=['accuracy'])

"""We fit the data for validation and training. Then take the batch size = 32 and epoch size = 30 """

batch = 32
epoch = 30

history = model.fit(X_train,y_train,batch_size= batch,epochs= epoch,verbose=1,validation_data=(X_test, y_test),shuffle=True)

"""#Evaluate the model"""

loss_and_metrics = model.evaluate(X_test,y_test)
print(loss_and_metrics)

"""#Test Model"""

from IPython.display import Image, display
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

TGREEN =  '\033[1;37;42m'
TRED =    '\033[1;37;41m'
TYELLOW = '\033[0;43m'

for i in range (1,7):
  img_directory = str(i) + '.jpeg'
  img_data = image.load_img(img_directory, target_size = (48, 48))   #load the image from the directory
  img_data = image.img_to_array(img_data)                            #convert the image to a Numpy array
  img_data = tf.image.rgb_to_grayscale(img_data)

  #print(img_data.shape)
  #img_data = np.array(img_data, 'float32')
  #img_data.resize(48,48,1)
  #print(img_data.shape)
  img_data = np.expand_dims(img_data, axis = 0)                     #expands the array by inserting a new axis at the specified position.
  #print(img_data.shape)

  classify = model.predict(img_data)
  display(Image(img_directory,width= 150, height=150))
  print("\n")
  max_index = np.argmax(classify[0])
  emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
  emotion_prediction = emotion_detection[max_index]  
  
  if(max_index == 3 or max_index == 5):
    print(TGREEN + str(max_index) + ' = ' +  emotion_prediction)
  elif(max_index == 4 or max_index == 2 or max_index == 0):
    print(TRED + str(max_index) + ' = ' +  emotion_prediction)
  else:
    print(TYELLOW + str(max_index) + ' = ' +  emotion_prediction)

"""#Save the model

We will serialize the model to JSON and save the model's weights in a hd5 file, so we can use it to make predictions directly without retraining the model everytime.
"""

model_json = model.to_json()
with open("model.json", "w") as json_file:
  json_file.write(model_json)
  model.save_weights("model.h5")

print("Saved model to disk")

"""The real time detection will be done using Jupiter notebook and the JSON file with the model and the weights. """