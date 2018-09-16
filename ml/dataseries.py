import glob
import random
import os
import numpy as np
import pandas as pd
import sklearn.preprocessing
from keras.utils.np_utils import to_categorical
import scipy.interpolate as interp

class DataSeries:
    def __init__(self, labelfunction, path, caselabels, classes, skiprows=1, include_only=None, regression=False):
        self.path = path
        self.caselabelspath = caselabels
        self.include_only = include_only
        self.skiprows = skiprows
        self.classes = classes
        self.n_classes = len(classes)
        self.regression = regression
        self.cases = self.get_cases()
        self.caselabels = labelfunction(self)


    def get_cases(self):
        cases = [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d)) and self.is_case_valid(d)]
        cases = sorted(cases)
        return cases

    def get_labels_by_case_ap_left_right(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                labels[case] = excelfile.loc[excelfile['Case ID'] == case, 'LeftVsRight'].values[0]
            except IndexError:
                print(f"Unable to find entry for {case}")
        return labels

    def get_labels_by_case_ap_lrs_regression(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                label_lrs = excelfile.loc[excelfile['Case ID'] == case, 'LRS'].values[0]
                label_ap = excelfile.loc[excelfile['Case ID'] == case, 'AP'].values[0]
                if not np.isnan(label_lrs) and not np.isnan(label_ap):
                    labels[case] = np.array([label_lrs, label_ap])
            except IndexError:
                print(f"Unable to find entry for {case}")
        return labels

    def get_labels_by_case_ap_left_right_septal_other(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                labels[case] = excelfile.loc[excelfile['Case ID'] == case, 'SeptalLateral'].values[0]
                if labels[case] == 'L':
                    labels[case] = excelfile.loc[excelfile['Case ID'] == case, 'LeftVsRight'].values[0]
                elif str(labels[case]) == 'nan':
                    labels[case] = 'O'
            except IndexError:
                print(f"Unable to find entry for {case} as {self.include_only} != 1")
        return labels

    def get_labels_by_case_ap_left_right_septal(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                labels[case] = excelfile.loc[excelfile['Case ID'] == case, 'SeptalLateral'].values[0]
                if labels[case] == 'L':
                    labels[case] = excelfile.loc[excelfile['Case ID'] == case, 'LeftVsRight'].values[0]
            except IndexError:
                print(f"Unable to find entry for {case} as {self.include_only} != 1")
        return labels

    def get_labels_by_case_ve_left_right(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                labels[case] = excelfile.loc[excelfile['Study number'] == case, 'LVvsRV'].values[0]
            except IndexError:
                print(f"Unable to find entry for {case}")
        return labels

    def get_labels_by_case_ve_right_leftbody_leftot(self):
        labels = {}
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        for case in self.cases:
            try:
                labels[case] = excelfile.loc[excelfile['Study number'] == case, 'RV=1,LVB=2,LVOT=3'].values[0]
            except IndexError:
                print(f"Unable to find entry for {case}")
        return labels

    def get_train_test_data(self, train_test_ratio=0.75, reverse=True, n_folds=4, fold_num=0, downsample_ratio=None):
        train_cases, test_cases = self.split_cases(train_test_ratio, n_folds=n_folds, fold_num=fold_num)
        croplength = self.get_longest_npy_file()
        if self.regression:
            train_x, train_y, train_n, train_caseids = self.data_and_labels_from_cases_regression(train_cases,
                                                                                                   croplength,
                                                                                                   downsample_ratio)
            test_x, test_y, test_n, test_caseids = self.data_and_labels_from_cases_regression(test_cases,
                                                                                               croplength,
                                                                                               downsample_ratio)
        else:
            train_x, train_y, train_n, train_caseids = self.data_and_labels_from_cases_categorical(train_cases,
                                                                                                   croplength,
                                                                                                   downsample_ratio)
            test_x, test_y, test_n, test_caseids = self.data_and_labels_from_cases_categorical(test_cases,
                                                                                               croplength,
                                                                                               downsample_ratio)

        if reverse:
            train_x = np.flip(train_x, axis=1)
            test_x = np.flip(test_x, axis=1)

        return (train_x, train_y, train_n, train_caseids), (test_x, test_y, test_n, test_caseids)

    def list_of_strings_to_onehot(self, list_of_strings, n_classes):
        list_of_integers = [self.classes.index(string) for string in list_of_strings]
        label_binarizer = sklearn.preprocessing.LabelBinarizer()
        label_binarizer.fit(range(max(list_of_integers) + 1))
        # if n_classes == 2: # Binary problem, labels are ints
        #     onehot = [value[0] for value in label_binarizer.transform(list_of_integers)]
        # else: # Categorical problem, labels are lists
        #     onehot = to_categorical(list_of_integers, n_classes)
        onehot = to_categorical(list_of_integers, n_classes)
        onehot = np.stack(onehot)
        return onehot

    @staticmethod
    def normalise_array(array):
        ''' NB THIS NORMALISES ALL COLUMNS EQUALLY - GOOD FOR ECGS, BUT USUALLY BAD
        np.nan REPLACED BY 0s AT END'''
        array -= np.nanmean(array)
        array /= np.nanstd(array)
        array = np.nan_to_num(array)
        return array

    def is_case_valid(self, case):
        excelfile = pd.read_excel(self.caselabelspath, skiprows=self.skiprows)
        if (not self.include_only) or (
                excelfile.loc[excelfile['Case ID'] == case, self.include_only[0]].values[0] == self.include_only[1]):
            return True

    def data_and_labels_from_cases_regression(self, cases, croplength, downsample_ratio=None):
        x = []
        y = []
        caseids = []
        n_cases = 0
        for case in cases:
            n_cases += 1
            try:
                caselabel = self.caselabels[case]
                npyfiles = glob.glob(os.path.join(self.path, case, "*.npy"))
                if not len(npyfiles):
                    print(f"Unable to find any npyfile for case {case}")
                for npyfile in npyfiles:
                    data = np.load(npyfile)
                    result = np.full((croplength, data.shape[1]), np.nan) #Create nans for where we don't have data
                    result[:data.shape[0], :data.shape[1]] = data

                    if downsample_ratio:
                        result = self.downsample_x(result, ratio=downsample_ratio)
                    caseids.append(case)
                    x.append(result)
                    y.append(caselabel)
            except KeyError:
                print(f"Unable to find label for {case}; skipping")
                pass
        x = np.stack(x)
        x = self.normalise_array(x)
        y = np.stack(y)

        return x, y, n_cases, caseids

    def data_and_labels_from_cases_categorical(self, cases, croplength, downsample_ratio=None):
        x = []
        y = []
        caseids = []
        n_cases = 0
        for case in cases:
            n_cases += 1
            try:
                caselabel = self.caselabels[case]
                npyfiles = glob.glob(os.path.join(self.path, case, "*.npy"))
                if not len(npyfiles):
                    print(f"Unable to find any npyfile for case {case}")
                for npyfile in npyfiles:
                    data = np.load(npyfile)
                    result = np.full((croplength, data.shape[1]), np.nan) #Create nans for where we don't have data
                    result[:data.shape[0], :data.shape[1]] = data

                    if caselabel and isinstance(caselabel, str):
                        if downsample_ratio:
                            result = self.downsample_x(result, ratio=downsample_ratio)
                        caseids.append(case)
                        x.append(result)
                        y.append(caselabel)
                    else:
                        print(f"Case {case} not used for some reason - likely missing a label")
                        pass
            except KeyError:
                print(f"Unable to find label for {case}; skipping")
                pass
        x = np.stack(x)
        x = self.normalise_array(x)
        y = self.list_of_strings_to_onehot(y, self.n_classes)

        return x, y, n_cases, caseids

    @staticmethod
    def downsample_x(x, ratio):
        x_len = x.shape[0]
        x_interp = interp.interp1d(np.arange(x_len), x, axis=0)
        x_compress = x_interp(np.linspace(0, x_len - 1, x_len*ratio))
        return x_compress

    def get_longest_npy_file(self):
        longestfilelength = 0
        npyfile_list = glob.glob(os.path.join(self.path, "**/*.npy"), recursive=True)
        for npyfile in npyfile_list:
            tmp = np.load(npyfile)
            if tmp.shape[0] > longestfilelength:
                longestfilelength = tmp.shape[0]
        return longestfilelength

    def split_cases(self, ratio=0.75, seed=86, n_folds=4, fold_num=0):
        cases = np.copy(self.cases)
        if seed:
            random.seed(seed)
        random.shuffle(cases)
        training_sample_length = len(cases) // n_folds
        test = cases[training_sample_length * fold_num:training_sample_length * (fold_num + 1)] #0:1, 1:2, 2:3, 3:4
        train = np.hstack((cases[:training_sample_length * fold_num], cases[training_sample_length * (fold_num + 1):])) #:0 & 1: , :1 & 2:
        return train, test