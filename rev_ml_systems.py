# !/user/bin/env python3

# This is used for calling/configuring all ML systems on the Revenant
# Thanks to https://www.kaggle.com/iomili/finger-counting-image-recognition-with-cnn for the code/dataset

import glob

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn import metrics
from tensorflow import lite as tflite
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from tensorflow.keras.models import Sequential

from rev_actions import ActionAccess
from rev_console_logger import ConsoleAccess

train_files = glob.glob("fingers/train/*.png")
test_files = glob.glob("fingers/test/*.png")

# Load tf model from file
interpreter = tflite.Interpreter('converted_model_fingers_cnn.tflite')
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']


# Having to resize as trying to run on 128x128 results in numpy maximum array size error
def resizer(large_image, size):
    return large_image.thumbnail(size, Image.ANTIALIAS)


def trainer():
    ConsoleAccess.console_printer("Training...")
    im = Image.open(train_files[0])
    plt.imshow(im)

    im_array = np.array(im)

    X_train = np.zeros((len(train_files), 64, 64))
    Y_train = np.zeros((len(train_files), 6))

    output_size = 64, 64

    for i, trf in enumerate(train_files):
        large_image = Image.open(trf)

        small_image = resizer(large_image, output_size)

        X_train[i, :, :] = np.array(small_image)
        Y_train[i, int(trf[-6:-5])] = 1

    X_test = np.zeros((len(test_files), 64, 64))
    Y_test = np.zeros((len(test_files), 6))

    for i, tsf in enumerate(test_files):
        large_image = Image.open(tsf)

        small_image = resizer(large_image, output_size)

        X_test[i, :, :] = np.array(small_image)
        Y_test[i, int(tsf[-6:-5])] = 1

    ConsoleAccess.console_printer("number of training examples = " + str(X_train.shape[0]))
    ConsoleAccess.console_printer("number of test examples = " + str(X_test.shape[0]))
    ConsoleAccess.console_printer("X_train shape: " + str(X_train.shape))
    ConsoleAccess.console_printer("Y_train shape: " + str(Y_train.shape))
    ConsoleAccess.console_printer("X_test shape: " + str(X_test.shape))
    ConsoleAccess.console_printer("Y_test shape: " + str(Y_test.shape))

    model = Sequential()
    model.add(
        Conv2D(64, (6, 6), strides=(1, 1), input_shape=(64, 64, 1), padding='same', activation='relu', use_bias=False))
    model.add(MaxPool2D((8, 8)))
    model.add(Conv2D(128, (6, 6), activation='relu', use_bias=False))
    model.add(Flatten())
    model.add(Dense(6, activation='softmax'))
    model.summary()

    X_train = X_train.reshape(X_train.shape[0], 64, 64, 1) / 255
    X_test = X_test.reshape(X_test.shape[0], 64, 64, 1) / 255

    model.compile('SGD', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=X_train, y=Y_train, batch_size=128, epochs=10, validation_split=0.2)

    Y_pred_test = model.predict_classes(X_test)

    ConsoleAccess.console_printer(metrics.confusion_matrix(np.argmax(Y_test, axis=1), Y_pred_test))

    ConsoleAccess.console_printer(metrics.classification_report(np.argmax(Y_test, axis=1), Y_pred_test, digits=3))

    cnn_model = model

    converter = tf.lite.TFLiteConverter.from_keras_model(cnn_model)

    tflite_model = converter.convert()
    open("converted_model_fingers_cnn_new.tflite", "wb").write(tflite_model)

    ConsoleAccess.console_printer(
        "------------------------------------------FINISHED------------------------------------------")


def read_fingers():
    # Perform inference and print output
    print("Analysing fingers...")
    input_data = np.array(ActionAccess.snap_pic_for_analysis(), dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(f'Number of fingers: {np.argmax(output_data)}.')
    print(f'Probability: {np.max(output_data)}.')


if __name__ == "__main__":
    # Perform a test on ML systems
    ConsoleAccess.console_print_enable = True
    while True:
        input("Hit enter to read fingers")
        read_fingers()
