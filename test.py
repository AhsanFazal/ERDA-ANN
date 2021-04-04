# Modify 'test1.jpg' and 'test2.jpg' to the images you want to predict on

from keras.models import load_model
from keras.preprocessing import image
import numpy as np

# dimensions of our images
img_width, img_height = 420, 280

# load the model we saved
model = load_model('./airline.h5')
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# predicting images
img = image.load_img('./data-mining/images/train/KLM Royal Dutch Airlines.Boeing.737.1cc2cee8-2f6c-457b-96b7-e50c0cbd5f96.jpg',
                     target_size=(img_width, img_height))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

images = np.vstack([x])
classes = model.predict_classes(images, batch_size=10)
print(classes)

# # predicting multiple images at once
# img = image.load_img('test2.jpg', target_size=(img_width, img_height))
# y = image.img_to_array(img)
# y = np.expand_dims(y, axis=0)

# # pass the list of multiple images np.vstack()
# images = np.vstack([x, y])
# classes = model.predict_classes(images, batch_size=10)

# # print the classes, the images belong to
# print classes
# print classes[0]
# print classes[0][0]
