import numpy as np
import pandas as pd
from pprint import pprint
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os


fileNames = os.listdir("./data-mining/images/train")
# Create empty lists to store values in later
airlines = []
airplaneModels = []

# Get the data from the file names
for fileName in fileNames:
    airline = fileName.split('.')[0]
    airplaneModel = fileName.split(
        '.')[1] + " " + fileName.split('.')[2]

    airlines.append(airline)
    airplaneModels.append(airplaneModel)

# Create a pandas dataframe
df = pd.DataFrame({
    'filename': fileNames,
    'airline': airlines,
    'airplaneModel': airplaneModels
})

# Define the model

img_width, img_height = 420, 280

train_data_dir = './data-mining/images/train'
validation_data_dir = './data-mining/images/validation'

nb_train_samples = 2000
nb_validation_samples = 800
epochs = 50
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)


test_datagen = ImageDataGenerator(rescale=1. / 255)


train_generator = train_datagen.flow_from_dataframe(
    df,
    directory="./data-mining/images/train",
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# validation_generator = test_datagen.flow_from_dataframe(
#     validation_data_dir,
#     target_size=(img_width, img_height),
#     batch_size=batch_size,
#     class_mode='binary')

model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    # validation_data=validation_generator,
    # validation_steps=nb_validation_samples // batch_size)
)
model.save_weights('first_try.h5')
