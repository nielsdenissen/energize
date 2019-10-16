from keras.applications.inception_v3 import InceptionV3
from keras.applications.xception import Xception
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.layers import Dense, Flatten, GlobalAveragePooling2D, Conv2D, ConvLSTM2D, Conv3D, MaxPooling2D, Dropout, \
    MaxPooling3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model, Sequential
from keras.utils import plot_model
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from keras.models import load_model, Model

import keras.layers
import os
import cv2
import numpy as np

from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16

import json


class ConvolutionalNNDropout(object):
    """
    2D Convolutional Neural Network implementing Dropout and batch normalization

    :param image_size: dimensions of input images
    :param channels: number of image channels
    :param emotion_map: dict of target emotion label keys with int values corresponding to the index of the emotion probability in the prediction output array
    :param filters: number of filters/nodes per layer in CNN
    :param kernel_size: size of sliding window for each layer of CNN
    :param activation: name of activation function for CNN
    :param verbose: if true, will print out extra process information

    **Example**::

        net = ConvolutionalNNDropout(target_dimensions=(64,64), channels=1, target_labels=[0,1,2,3,4,5,6], time_delay=3)
        net.fit(features, labels, validation_split=0.15)

    """

    def __init__(self, image_size, emotion_map, filters=10, kernel_size=(4, 4), activation='relu',
                 verbose=False, model_filepath = None):
        self.image_size = image_size
        self.verbose = verbose
        self.channels = 1

        self.emotion_map = emotion_map

        self.filters = filters
        self.kernel_size = kernel_size
        self.activation = activation
        self.model = None
        self.load_model(model_filepath)

    def _init_model(self):
        """
        Composes all layers of 2D CNN.
        """
        model = Sequential()
        model.add(Conv2D(input_shape=list(self.image_size) + [self.channels], filters=self.filters,
                         kernel_size=self.kernel_size, activation='relu', data_format='channels_last', kernel_regularizer=l2(0.01)))
        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D())
        model.add(Dropout(0.5))

        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D())
        model.add(Dropout(0.5))

        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D())
        model.add(Dropout(0.5))

        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(
            Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D())
        model.add(Dropout(0.5))

        model.add(Flatten())

        model.add(Dense(units=len(self.emotion_map.keys()), activation="softmax"))
        if self.verbose:
            model.summary()
        self.model = model

    def fit(self, image_data, labels, validation_split, epochs=50, class_weights = None):
        """
        Trains the neural net on the data provided.

        :param image_data: Numpy array of training data in shape (num_samples, image_size[0], image_size[1], num_channels)
        :param labels: Numpy array of target (label) data in shape (num_samples, num_categories) (one-hot encoded)
        :param validation_split: Float between 0 and 1. Percentage of training data to use for validation
        :param batch_size:
        :param epochs: number of times to train over input dataset.
        """
        self.model.compile(optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7), loss=categorical_crossentropy, metrics=['accuracy'])
        self.model.fit(image_data, labels, epochs=epochs, validation_split=validation_split,
                       callbacks=[ReduceLROnPlateau(), EarlyStopping(patience=3)], class_weight = class_weights)

    def predict(self, image_data):
        """

        :param image_data: Numpy array of training data in shape (num_samples, image_size[0], image_size[1], num_channels)
        :return:
        """


        return self.model.predict(image_data)

    def predict_from_faces(self, faces):
        """

        :param faces: list of faces (each a 2d numpy array, of different sizes)
        :return:
        """
        resized_faces = np.array([cv2.resize(face, self.image_size, interpolation=cv2.INTER_CUBIC) for face in faces])
        # add channel
        resized_faces = np.expand_dims(resized_faces, axis = -1)

        predictions = np.argmax(self.predict(resized_faces), axis = 1)
        predictions = [self.emotion_map[i] for i in predictions]
        return predictions


    def load_model(self, model_filepath):
        # TODO:Load pickle
        if model_filepath and os.path.isfile(model_filepath) :
            print(f"Loading existing model at {model_filepath}")
            self.model = load_model(model_filepath)

        else:
            self._init_model()
            print("Creating a new model")

    def save_model(self, model_filepath):
        # TODO: Save as pickle
        raise NotImplementedError("save_model not implemented")


class TransferLearningNN(object):
    """
    2D Convolutional Neural Network implementing Dropout and batch normalization

    :param image_size: dimensions of input images
    :param channels: number of image channels
    :param emotion_map: dict of target emotion label keys with int values corresponding to the index of the emotion probability in the prediction output array
    :param filters: number of filters/nodes per layer in CNN
    :param kernel_size: size of sliding window for each layer of CNN
    :param activation: name of activation function for CNN
    :param verbose: if true, will print out extra process information

    **Example**::

        net = ConvolutionalNNDropout(target_dimensions=(64,64), channels=1, target_labels=[0,1,2,3,4,5,6], time_delay=3)
        net.fit(features, labels, validation_split=0.15)

    """

    def __init__(self, image_size, filters=10, kernel_size=(4, 4), activation='relu',
                 verbose=False, model_filepath = None, emotion_map = None, emotion_map_filepath = None):
        self.image_size = image_size
        self.verbose = verbose
        self.channels = 3

        self.emotion_map = emotion_map

        self.filters = filters
        self.kernel_size = kernel_size
        self.activation = activation
        self.model = None

        self.load_model(model_filepath)


    def _init_model(self):
        """
        Composes all layers of 2D CNN.
        """

        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=list(self.image_size) + [self.channels])
        x = base_model.output
        x = Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.MaxPooling2D()(x)
        x = keras.layers.Dropout(0.5)(x)
        x = Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.MaxPooling2D()(x)
        x = keras.layers.Dropout(0.5)(x)
        x = Conv2D(filters=self.filters, kernel_size=self.kernel_size, activation='relu', data_format='channels_last', padding='same')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.MaxPooling2D()(x)
        x = keras.layers.Dropout(0.5)(x)

        x = keras.layers.Flatten()(x)
        predictions = keras.layers.Dense(units=len(self.emotion_map.keys()), activation="softmax")(x)

        model = Model(inputs=base_model.input, outputs=predictions)

        for layer in base_model.layers:
            layer.trainable = False
        if self.verbose:
            model.summary()
        self.model = model

    def fit(self, image_data, labels, validation_split, epochs=50, class_weights = None):
        """
        Trains the neural net on the data provided.

        :param image_data: Numpy array of training data in shape (num_samples, image_size[0], image_size[1], num_channels)
        :param labels: Numpy array of target (label) data in shape (num_samples, num_categories) (one-hot encoded)
        :param validation_split: Float between 0 and 1. Percentage of training data to use for validation
        :param batch_size:
        :param epochs: number of times to train over input dataset.
        """
        self.model.compile(optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7), loss=categorical_crossentropy, metrics=['accuracy'])
        self.model.fit(image_data, labels, epochs=epochs, validation_split=validation_split,
                       callbacks=[ReduceLROnPlateau(), EarlyStopping(patience=3)])

    def predict(self, image_data):
        """

        :param image_data: Numpy array of training data in shape (num_samples, image_size[0], image_size[1], num_channels)
        :return:
        """


        return self.model.predict(image_data)

    def predict_from_faces(self, faces):
        """

        :param faces: list of faces (each a 2d numpy array, of different sizes)
        :return:
        """
        resized_faces = np.array([cv2.resize(face, self.image_size, interpolation=cv2.INTER_CUBIC) for face in faces])
        # add channel
        resized_faces = np.expand_dims(resized_faces, axis = -1)

        predictions = np.argmax(self.predict(resized_faces), axis = 1)
        predictions = [self.emotion_map[i] for i in predictions]
        return predictions


    def load_model(self, model_filepath):
        # TODO:Load pickle
        if model_filepath and os.path.isfile(model_filepath):
            print(f"Loading existing model at {model_filepath}")
            self.model = load_model(model_filepath)

        else:
            print("Creating a new model")
            self._init_model()

    def save_model(self, model_filepath, emotion_map_filepath):
        # TODO: Save as pickle
        self.model.save(model_filepath)
        if emotion_map_filepath is not None:
            self.save_emotion_map()
        #raise NotImplementedError("save_model not implemented")

    def save_emotion_map(self, emotion_map_filepath):
        # TODO: Save emotion_map when saving the model
        with open(emotion_map_filepath, 'w') as fp:
            json.dump(self.emotion_map, fp)

    def load_emotion_map(self, emotion_map_filepath):
        # TODO: Load emotion_map when loading a model
        with open(emotion_map_filepath) as f_in:
            self.emotion_map= json.load(f_in)