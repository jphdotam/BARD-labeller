from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, AtrousConv1D

from ml.network import Network

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Best_LSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(AtrousConv1D(64, 5, atrous_rate=2, input_shape=(sequence_length, input_channels)))
        #self.model.add(Dropout(0.2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        #self.model.add(Dropout(0.2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        #self.model.add(Dropout(0.2))

        self.model.add(LSTM(64, input_shape=(sequence_length,input_channels), dropout=0.2, return_sequences=True))
        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

class Best_LSTM_binary(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(AtrousConv1D(64, 5, atrous_rate=2, input_shape=(sequence_length, input_channels)))
        #self.model.add(Dropout(0.2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        #self.model.add(Dropout(0.2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        #self.model.add(Dropout(0.2))

        self.model.add(LSTM(64, input_shape=(sequence_length,input_channels), dropout=0.2, return_sequences=True))
        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss="binary_crossentropy", optimizer='adamax', metrics=['accuracy'])


class Best_BiLSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(Bidirectional(LSTM(64, dropout=0.2, return_sequences=True),input_shape=(sequence_length,input_channels)))
        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

