# Modify 'test1.jpg' and 'test2.jpg' to the images you want to predict on

from keras.models import load_model
from keras.preprocessing import image
import numpy as np

# dimensions of our images
img_width, img_height = 420, 280

loaded_model = load_model('airline.h5')

test = loaded_model.layers[0].input_shape  # (None, 160, 160, 3)

print(test)
