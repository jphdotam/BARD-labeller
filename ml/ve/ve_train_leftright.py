from ml.ve.ve_models import Best_LSTM_categorical, Best_BiLSTM_categorical, Best_LSTM_binary
import numpy as np
from ml.training_utils import plot_by_fold, get_distribution_of_labels_categorical_from_caselabels
from ml.dataseries import DataSeries

dataseries = DataSeries(path="../../exports/ve-qrst",
                        labelfunction=DataSeries.get_labels_by_case_ve_left_right,
                        #caselabels="C:\\Users\\J\\Box Sync\\CLAIM-Data\\CLAIM-VE\\james_labels.xlsx",
                        caselabels="C:\\Users\\James\\Box\\CLAIM-Data\\CLAIM-VE\\james_labels.xlsx",
                        n_classes=2)

valaccuracy_by_fold = []
valloss_by_fold = []
prop_by_fold = []
verbose = 1

modeltype = Best_LSTM_binary
downsample_ratio = 0.1

print(get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

for fold in range(4):
    print(f"FOLD {fold}")
    (train_x, train_y, train_n), (test_x, test_y, test_n) = dataseries.get_train_test_data(reverse=True, fold_num=fold,
                                                                                           downsample_ratio=downsample_ratio)

    seq_length = train_x.shape[1]
    input_channels = train_x.shape[2]

    if fold == 0:
        print(f"Train: {train_x.shape}")
        print(f"Test: {test_x.shape}")

    model = modeltype(sequence_length=seq_length, input_channels=input_channels, n_classes=2)

    results = model.train(train_x, train_y, epochs=5, batch_size=32, tensorboard_modelname="3cat",
                          validation_data=(test_x, test_y), verbose=verbose)

    valaccuracy_by_fold.append(results.history['val_acc'])
    valloss_by_fold.append(results.history['val_loss'])

valaccuracy_by_fold = np.stack(valaccuracy_by_fold)
valloss_by_fold = np.stack(valloss_by_fold)

print(get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

plot_by_fold(valaccuracy_by_fold, valloss_by_fold)
