from ml.ap.ap_models import Best_CNN_categorical, Best_LSTM_categorical, Best_CNN_LSTM_categorical, \
    Best_BiLSTM_categorical, Best_aCNN_categorical
import numpy as np
from ml.training_utils import plot_by_fold, get_distribution_of_labels_categorical_from_caselabels, \
    class_weights_from_onehot_categorical
from ml.dataseries import DataSeries
import pandas as pd

dataseries = DataSeries(path="../../exports/ap_qrs_all",
                        labelfunction=DataSeries.get_labels_by_case_ap_left_right,
                        #caselabels="C:\\Users\\J\\Box Sync\\CLAIM-Data\\CLAIM-AP\\test.xlsx",
                        caselabels="C:\\Users\\James\\Box\\CLAIM-Data\\CLAIM-AP\\test.xlsx",
                        classes=['L','R'],
                        include_only=("NN2",1))

valaccuracy_by_fold = []
valloss_by_fold = []
prop_by_fold = []
verbose = 2

modeltype = Best_aCNN_categorical
downsample_ratio = 0.4

results_dict = {}

print(get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

for fold in range(4):
    print(f"FOLD {fold}")
    (train_x, train_y, train_n, train_caseids),\
    (test_x, test_y, test_n, test_caseids) = dataseries.get_train_test_data(reverse=True, fold_num=fold,
                                                                            downsample_ratio=downsample_ratio)

    seq_length = train_x.shape[1]
    input_channels = train_x.shape[2]

    if fold == 0:
        print(f"Train: {train_x.shape} from {train_n} cases")
        print(f"Test: {test_x.shape} from {test_n} cases")

    model = modeltype(sequence_length=seq_length, input_channels=input_channels, n_classes=3)

    results = model.train(train_x, train_y, epochs=10, batch_size=32, tensorboard_modelname=f"cnn_lstm_newcat_{fold}",
                          validation_data=(test_x, test_y), verbose=verbose)

    print(f"Categories are {list(enumerate(dataseries.classes))}")
    predictions_by_case = {caseid:[] for caseid in set(test_caseids)}
    answers_by_case = {}
    for case, x, y in zip(test_caseids, test_x, test_y):
        x = x.reshape(1, x.shape[0], x.shape[1])
        predictions_by_case[case].append(model.predict(x)[0])
        answers_by_case[case] = y
    for case in predictions_by_case.keys():
        result = np.mean(np.stack(predictions_by_case[case]),axis=0)
        if np.argmax(result) == np.argmax(answers_by_case[case]):
            correct = "CORRECT"
        else:
            correct = "INCORRECT"
        print(f"CASE {case}: {result} - {correct}")
        results_dict[case] = [result[0], result[1], result[2], np.argmax(result), np.argmax(answers_by_case[case]), correct]

    # print(f"Categories are {list(enumerate(dataseries.classes))}")
    # for case, x, y in zip(train_caseids, train_x, train_y):
    #     x = x.reshape(1, x.shape[0], x.shape[1])
    #     result = model.predict(x)
    #     if np.argmax(result) == np.argmax(y):
    #         correct = "CORRECT"
    #     else:
    #         correct = "INCORRECT"
    #     print(f"TRAIN: I think case {case} is {result} - should be {y} - {correct}")
    # for case, x, y in zip(test_caseids, test_x, test_y):
    #     x = x.reshape(1, x.shape[0], x.shape[1])
    #     result = model.predict(x)
    #     if np.argmax(result) == np.argmax(y):
    #         correct = "CORRECT"
    #     else:
    #         correct = "INCORRECT"
    #     print(f"TEST: I think case {case} is {result} - should be {y} - {correct}")

    valaccuracy_by_fold.append(results.history['val_acc'])
    valloss_by_fold.append(results.history['val_loss'])

valaccuracy_by_fold = np.stack(valaccuracy_by_fold)
valloss_by_fold = np.stack(valloss_by_fold)

pd.DataFrame.from_dict(results_dict,orient='index').to_csv("ap_results.csv")

print(get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

plot_by_fold(valaccuracy_by_fold, valloss_by_fold)
