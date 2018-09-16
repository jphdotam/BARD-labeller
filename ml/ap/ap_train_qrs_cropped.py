from ml.ap.ap_models import Best_CNN_categorical, Best_LSTM_categorical, Best_CNN_LSTM_categorical, \
    Best_BiLSTM_categorical
import numpy as np
import ml.training_utils
from ml.dataseries import DataSeries

dataseries = DataSeries(path="../../exports/ap_qrs_95",
                        labelfunction=DataSeries.get_labels_by_case_ap_left_right_septal,
                        caselabels="C:\\Users\\J\\Box Sync\\CLAIM-Data\\CLAIM-AP\\james_labels.xlsx",
                        n_classes=3)

valaccuracy_by_fold = []
valloss_by_fold = []
prop_by_fold = []
verbose = 2

modeltype = Best_BiLSTM_categorical
downsample_ratio = 0.3

cropped_length = 30

print(ml.training_utils.get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

for fold in range(4):
    print(f"FOLD {fold}")
    (train_x, train_y), (test_x, test_y) = dataseries.get_train_test_data(reverse=True, fold_num=fold,
                                                                          downsample_ratio=downsample_ratio)

    train_x = ml.training_utils.crop_x_to_length(train_x, cropped_length)
    test_x = ml.training_utils.crop_x_to_length(test_x, cropped_length)

    seq_length = train_x.shape[1]
    input_channels = train_x.shape[2]

    if fold == 0:
        print(f"Train: {train_x.shape}")
        print(f"Test: {test_x.shape}")

    model = modeltype(sequence_length=seq_length, input_channels=input_channels, n_classes=3)

    results = model.train(train_x, train_y, epochs=20, batch_size=32, tensorboard_modelname="3cat",
                          validation_data=(test_x, test_y), verbose=verbose)

    valaccuracy_by_fold.append(results.history['val_acc'])
    valloss_by_fold.append(results.history['val_loss'])

valaccuracy_by_fold = np.stack(valaccuracy_by_fold)
valloss_by_fold = np.stack(valloss_by_fold)

print(ml.training_utils.get_distribution_of_labels_categorical_from_caselabels(dataseries.caselabels))

ml.training_utils.plot_by_fold(valaccuracy_by_fold, valloss_by_fold)
