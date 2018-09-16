from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, SeparableConv1D, LSTM, Bidirectional, AtrousConv1D, GRU

from ml.network import Network

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Best_CNN_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu',
                                       input_shape=(sequence_length, input_channels)))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Flatten())

        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])


class Best_aCNN_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(AtrousConv1D(64, 5, atrous_rate=2, input_shape=(sequence_length, input_channels)))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))

        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

class Best_aCNN_regression(Network):

    def __init__(self, sequence_length, input_channels, n_classes):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(AtrousConv1D(64, 5, atrous_rate=2, input_shape=(sequence_length, input_channels)))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))
        self.model.add(AtrousConv1D(32, 3, atrous_rate=2))

        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(n_classes, activation='linear'))
        self.model.compile(loss="mean_squared_error", optimizer='adamax')


class Best_SepCNN_LSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(SeparableConv1D(filters=32, kernel_size=3, padding='valid', activation='relu',
                                       input_shape=(sequence_length, input_channels)))

        self.model.add(SeparableConv1D(filters=64, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(SeparableConv1D(filters=64, kernel_size=3, padding='valid', activation='relu'))

        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

        print(self.model.summary())

class Best_CNN_LSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(Conv1D(filters=32, kernel_size=3, padding='valid', activation='relu',
                                       input_shape=(sequence_length, input_channels)))

        self.model.add(Conv1D(filters=64, kernel_size=3, padding='valid', activation='relu'))
        self.model.add(Conv1D(filters=64, kernel_size=3, padding='valid', activation='relu'))

        self.model.add(LSTM(64, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

class Best_LSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(LSTM(64, input_shape=(sequence_length,input_channels), dropout=0.2,  return_sequences=False))
        #self.model.add(LSTM(32, dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))
            #self.model.add(Dropout(0.2))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

class Best_BiLSTM_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, dense=True):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        self.model.add(Bidirectional(LSTM(32, dropout=0.2, recurrent_dropout=0.2, return_sequences=True), input_shape=(sequence_length,input_channels)))
        self.model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2, return_sequences=False))

        if dense:
            self.model.add(Dense(512, activation='relu'))
            self.model.add(Dropout(0.2))

        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

class Dynamic_CNN_binary(Network):

    def __init__(self, sequence_length, input_channels, conv_layers, kernel_size, n_filters, dropout, sepconv,
                 n_denses=1, dense_dropout=False, n_neurons_in_dense=512):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        for n_layer in range(conv_layers):
            if n_layer == 0:
                n_filt = n_filters[0]
                if sepconv:
                    self.model.add(
                        SeparableConv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                        input_shape=(sequence_length, input_channels)))
                else:
                    self.model.add(
                        Conv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                               input_shape=(sequence_length, input_channels)))

                if dropout:
                    self.model.add(Dropout(0.5))

            else:
                if n_layer < conv_layers-1:
                    n_filt = n_filters[1]
                else:
                    n_filt = n_filters[2]

                if sepconv:
                    self.model.add(
                        SeparableConv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                               input_shape=(sequence_length, input_channels)))
                else:
                    self.model.add(
                        Conv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                        input_shape=(sequence_length, input_channels)))
                if dropout:
                    self.model.add(Dropout(0.5))
                if n_layer < conv_layers-1:
                    self.model.add(MaxPooling1D(2))

        self.model.add(Flatten())

        for n_dense in range(n_denses):
            self.model.add(Dense(n_neurons_in_dense, activation='relu'))
            if dense_dropout:
                self.model.add(Dropout)
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss="binary_crossentropy", optimizer='adamax', metrics=['accuracy'])


class Dynamic_CNN_categorical(Network):

    def __init__(self, sequence_length, input_channels, n_classes, conv_layers, kernel_size, n_filters, dropout, sepconv,
                 n_denses=1, dense_dropout=False, n_neurons_in_dense=512):
        self.sess = tf.Session()
        K.set_session(self.sess)

        self.model = Sequential()

        for n_layer in range(conv_layers):
            if n_layer == 0:
                n_filt = n_filters[0]
                if sepconv:
                    self.model.add(
                        SeparableConv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                        input_shape=(sequence_length, input_channels)))
                else:
                    self.model.add(
                        Conv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                               input_shape=(sequence_length, input_channels)))

                if dropout:
                    self.model.add(Dropout(0.5))

            else:
                if n_layer < conv_layers-1:
                    n_filt = n_filters[1]
                else:
                    n_filt = n_filters[2]

                if sepconv:
                    self.model.add(
                        SeparableConv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                               input_shape=(sequence_length, input_channels)))
                else:
                    self.model.add(
                        Conv1D(filters=n_filt, kernel_size=kernel_size, padding='same', activation='relu',
                                        input_shape=(sequence_length, input_channels)))
                if dropout:
                    self.model.add(Dropout(0.5))
                if n_layer < conv_layers-1:
                    self.model.add(MaxPooling1D(2))

        self.model.add(Flatten())

        for n_dense in range(n_denses):
            self.model.add(Dense(n_neurons_in_dense, activation='relu'))
            if dense_dropout:
                self.model.add(Dropout)
        self.model.add(Dense(n_classes, activation='sigmoid'))
        self.model.compile(loss="categorical_crossentropy", optimizer='adamax', metrics=['accuracy'])

        #print(self.model.summary())
