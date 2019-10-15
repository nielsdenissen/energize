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
from keras.models import load_model
import os

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
        self._init_model()

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

        model.add(Flatten())

        model.add(Dense(units=len(self.emotion_map.keys()), activation="softmax"))
        if self.verbose:
            model.summary()
        self.model = model

    def fit(self, image_data, labels, validation_split, epochs=50):
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
