import os
import numpy as np
import pandas as pd
from pprint import pprint
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K


trainingFileNames = os.listdir("./data-mining/images/train")
# Create empty lists to store values in later
trainingAirlines = []
trainingAirplaneModels = []
trainingAirplaneManufactureres = []

# Get the data from the file names
for fileName in trainingFileNames:
    data = fileName.split('.')

    trainingAirlines.append(data[0])
    trainingAirplaneModels.append(data[2])
    trainingAirplaneManufactureres.append(data[1])

# Create a pandas dataframe
trainingDataFrame = pd.DataFrame({
    'fileName': trainingFileNames,
    'airline': trainingAirlines,
    'airplaneManufacturer': trainingAirplaneManufactureres,
    'airplaneModel': trainingAirplaneModels
})

validationFileNames = os.listdir("./data-mining/images/validation")
# Create empty lists to store values in later
validationAirlines = []
validationAirplaneModels = []
validationAirplaneManufactureres = []

# Get the data from the file names
for fileName in validationFileNames:
    data = fileName.split('.')

    validationAirlines.append(data[0])
    validationAirplaneModels.append(data[2])
    validationAirplaneManufactureres.append(data[1])

# Create a pandas dataframe
validationDataFrame = pd.DataFrame({
    'fileName': validationFileNames,
    'airline': validationAirlines,
    'airplaneManufacturer': validationAirplaneManufactureres,
    'airplaneModel': validationAirplaneModels
})

# Define the model

img_width, img_height = 420, 280

trainingDataDirectory = './data-mining/images/train'
validationDataDirectory = './data-mining/images/validation'

nb_train_samples = 1888
nb_validation_samples = 220
epochs = 2
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


def runModelFor(type):
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
                  optimizer='rmsprop', metrics=['accuracy'])

    trainDataGenerator = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False
    )

    validationDataGenerator = ImageDataGenerator(rescale=1. / 255)

    train_generator = trainDataGenerator.flow_from_dataframe(
        trainingDataFrame,
        directory=trainingDataDirectory,
        x_col="fileName",
        y_col=type,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')

    validationGenerator = validationDataGenerator.flow_from_dataframe(
        validationDataFrame,
        directory=validationDataDirectory,
        x_col="fileName",
        y_col=type,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')

    model.fit(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validationGenerator,
        validation_steps=nb_validation_samples // batch_size
    )

    model.save(type + '.h5')


runModelFor('airline')
runModelFor('airplaneManufacturer')
runModelFor('airplaneModel')
