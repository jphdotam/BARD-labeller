import numpy as np
from sklearn import svm
import pandas as pd
import os

def transform_2d_label_to_1d(label):
    return (label[0] * 3) + label[1]

def transform_2d_label_to_lateral(label):
    return label[0]

def accuracy_from_prediction_and_labels(predictions, labels, printres=True):
    total = 0
    correct_lateral = 0
    correct_ap = 0
    exact = 0
    for prediction, label in zip(predictions, labels):
        total+= 1
        if prediction // 3 == label // 3:
            correct_lateral +=1
        if prediction % 3 == label % 3:
            correct_ap += 1
        if prediction == label:
            exact += 1
    if printres:
        print(f"TOTAL: {total} cases")
        print(f"LATERAL: {correct_lateral/total*100} ({correct_lateral} cases)")
        print(f"AP: {correct_ap/total*100} ({correct_ap} cases)")
        print(f"EXACT: {exact/total*100} ({exact} cases)")

    return exact, correct_lateral, correct_ap, total

grand_total = 0
grand_lat = 0
grand_ap = 0
grand_exact = 0

for fold in range(4):
    print(os.getcwd())
    train_file = f"./ap_results_regression_train_fold_{fold}.csv"
    test_file = f"./ap_results_regression_test_fold_{fold}.csv"

    df_train = pd.read_csv(train_file)
    df_test = pd.read_csv(test_file)

    train_x = df_train.iloc[:, 1:3].as_matrix()
    train_y = np.stack([transform_2d_label_to_1d(label) for label in df_train.iloc[:,3:].as_matrix()])

    test_x = df_test.iloc[:, 1:3].as_matrix()
    test_y = np.stack([transform_2d_label_to_1d(label) for label in df_test.iloc[:, 3:].as_matrix()])

    clf = svm.SVC(kernel='linear',probability=True)
    clf.fit(train_x, train_y)
    test_result = clf.predict(test_x)
    test_proba = clf.predict_proba(test_x)

    acc = accuracy_from_prediction_and_labels(test_result,test_y)
    # grand_total += acc[3]
    # grand_exact += acc[0]
    # grand_lat += acc[1]
    # grand_ap += acc[2]
    # lat = {acc[1] / acc[3]}
    # ap = {acc[2] / acc[3]}
    # exact = {acc[0] / acc[3]}
    # print(f"Fold {fold}")
    # print(f"Lateral {lat}")
    # print(f"AP {ap}")
    # print(f"Exact {exact}\n\n")

    filtered_test_result, filtered_test_y = [],[]
    for result,proba,y in zip(test_result, test_proba, test_y):
        if np.max(proba > 0.65):
            filtered_test_result.append(result)
            filtered_test_y.append(y)
    acc = accuracy_from_prediction_and_labels(filtered_test_result,filtered_test_y)


print(f"GRAND")
print(f"Lateral {grand_lat/grand_total}")
print(f"AP {grand_ap/grand_total}")
print(f"Exact {grand_exact/grand_total}")
