import matplotlib.pyplot as plt
import numpy as np
import math

def plot_by_fold(valaccuracy, valloss, n_folds=4):
    for i in range(n_folds):
        plt.plot(valaccuracy[i], "m+-")
        plt.plot(valloss[i], "co-")
    plt.plot(np.mean(valaccuracy, axis=0), "r+-")
    plt.plot(np.mean(valloss, axis=0), "bo-")
    plt.show()

def crop_x_to_length(x, length):
    return x[:, -length:, :]

def get_distribution_of_labels_categorical_from_y(labels):
    label_counts = {}
    label_percentages = {}
    total_count = 0
    for label in labels:
        total_count += 1
        label_id = np.argmax(label)
        if label_id not in label_counts:
            label_counts[label_id] = 1
        else:
            label_counts[label_id] += 1
    for label_id in label_counts.keys():
        label_percentages[label_id] = (label_counts[label_id] / total_count) * 100
    return label_counts, label_percentages

def get_distribution_of_labels_categorical_from_caselabels(caselabels):
    labels = []
    label_counts = {}
    label_percentages = {}
    for label in caselabels.keys():
        if str(caselabels[label]) != 'nan':
            labels.append(caselabels[label])
    for category in set(labels):
        label_counts[category] = labels.count(category)
        label_percentages[category] = (labels.count(category) / len(labels)) * 100
    return label_counts, label_percentages

def get_class_weights_categorical_from_caselabels(caselabels):
    labels = []
    label_weights = {}
    for label in caselabels.keys():
        if str(caselabels[label]) != 'nan':
            labels.append(caselabels[label])
    for category in set(labels):
        label_weights[category] = 1/(labels.count(category) / len(labels))
    return label_weights

def class_weights_from_onehot_categorical(onehot):
    class_counts = {key:0 for key in range(onehot.shape[1])}
    class_weights = {key: 0 for key in range(onehot.shape[1])}
    for row in onehot:
        class_counts[np.argmax(row)] += 1
    for key in class_counts.keys():
        class_weights[key] = 1 / (class_counts[key] / onehot.shape[0])
    return class_weights

def get_distribution_of_labels_binary(labels):
    total = 0
    one = 0
    for label in labels:
        total += 1
        if label:
            one += 1
    return one, (one/total)*100