# Type your code here
import os
import json
import warnings
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

train_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet_v3.preprocess_input)
train_generator = train_datagen.flow_from_directory('data', target_size=(244,244), batch_size = 32, class_mode = 'categorical')
base_model = MobileNetV3Small(weights = 'imagenet', include_top = False, input_shape = (244, 244, 3))
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation = 'relu')(x)
predictions = Dense(train_generator.num_classes, activation = 'softmax')(x)
model = Model(inputs = base_model.input, outputs = predictions)

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.fit(train_generator, epochs = 5)

class_names = list(train_generator.class_indices.keys())
with open(os.path.join('models', 'class_names.json'), 'w') as f:
    json.dump(class_names, f)
model.save(os.path.join('models', 'my_model.h5'))
print('Done!')

