import pandas as pd
from io import StringIO
import pickle
import scipy.signal as signal
import scipy
import pywt  # conda install pywavelets
from math import sqrt, log2
from statsmodels.robust import mad
import numpy as np


class TxtFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.labelpath = filepath + '.label'
        self.channels, self.sample_freq, self.data = self.load_file()
        self.labels = self.load_labels()
        print("Channels: {}".format(self.channels))

    def load_file(self):
        with open(self.filepath) as f:
            channels, sample_freq = self.load_channels(f)
            _ = self._read_until(f, "[Data]")
            data = f.read()
            data = pd.read_table(StringIO(data), names=channels, sep=',')
            # data = self.filter_data(data)
            return channels, sample_freq, data

    @staticmethod
    def filter_data(data, type='wavelet', sample_freq=1000, savgol_filter=True):
        def waveletSmooth(x, wavelet="coif5", level=1):
            # Thanks to http://connor-johnson.com/2016/01/24/using-pywavelets-to-remove-high-frequency-noise/
            coefficients = pywt.wavedec(x, wavelet, mode="per")  # coefficients
            sigma = mad(coefficients[-level])  # sigma for thresholding
            uthresh = sigma * np.sqrt(2 * np.log(len(x)))  # thresholding value
            coefficients[1:] = (pywt.threshold(coefficient, value=uthresh, mode="soft") for coefficient in
                                coefficients[1:])  # threshold the coefficients
            y = pywt.waverec(coefficients, wavelet, mode="per")  # reconstruct
            return y
        if type == 'fir':
            nyq_rate = sample_freq / 2
            width = 5 / nyq_rate
            ripple_db = 100
            N, beta = signal.kaiserord(ripple_db, width)
            cutoff_hz = 30
            taps = signal.firwin(N, cutoff_hz / nyq_rate, window=("kaiser", beta))
            filtered_data = signal.lfilter(taps, 1.0, data)
            return filtered_data
        elif type == 'fft':
            fft = scipy.fft(data)
            bandpass_fft = fft[:]
            for i in range(len(fft)):
                if i >= 6000:
                    fft[i] = 0
            ifft = scipy.ifft(bandpass_fft)
            data = ifft.real
            if savgol_filter:
                data = signal.savgol_filter(data, window_length=21, polyorder=1)
            return data
        elif type == 'wavelet':
            data = waveletSmooth(data)
            return data
        else:
            print("UNKNOWN FILTER: {}".format(type))

    def load_channels(self, file):
        channels = []
        line = self._read_until(file, "Channels exported")
        sample_freq = int(self._read_until(file, "Sample Rate").rsplit(' ', 1)[-1].rsplit('Hz')[0])
        n_channels = int(line.split(' ')[-1])
        for n_channel in range(n_channels):
            line = self._read_until(file, "Label:")
            channel_name = line.split(' ')[-1].rstrip()
            channels.append(channel_name)
        return channels, sample_freq

    def load_labels(self):
        try:
            with open(self.labelpath, 'rb') as f:
                labels = pickle.load(f)
        except FileNotFoundError:
            print("Label file not found, creating new label file")
            labels = {}
            with open(self.labelpath, 'wb') as f:
                pickle.dump(labels, f)
        return labels

    def save_labels(self):
        with open(self.labelpath, 'wb') as f:
            pickle.dump(self.labels, f)

    def get_labels_by_type(self, labeltype):
        ranges = []
        for label in self.labels:
            if label['type'] == labeltype:
                ranges.append(label)

    @staticmethod
    def get_labels_from_textfile(textfile):
        """Used by the bard_ui to get the number of labels in the file preview"""
        labelfile = textfile + ".label"
        try:
            with open(labelfile, 'rb') as f:
                labels = pickle.load(f)
                return labels
        except (FileNotFoundError, EOFError):
            return []

    @staticmethod
    def _read_until(file, string):
        line = file.readline()
        while string not in line:
            line = file.readline()
        return line


if __name__ == "__main__":
    txtfile = TxtFile("../data/1001/1001_1.txt")
