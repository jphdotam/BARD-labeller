from ml.ap.ap_models import Dynamic_CNN_categorical
import numpy as np
import pandas as pd

if __name__ == "__main__":

    from ml.dataseries import DataSeries

    dataseries = DataSeries(path="../exports/ap_qrs_delta_95",
                            labelfunction=DataSeries.get_labels_by_case_ap_left_right_septal,
                            n_classes=3,
                            caselabels="C:\\Users\\J\\Box Sync\\CLAIM-Data\\CLAIM-AP\\james_labels.xlsx")

    run = 0
    result_table = []
    for conv_layers in range(2,5):
        print(f"n Conv Layers: {conv_layers}")
        for kernel_size in (3,5,7):
            print(f"Kernel size: {kernel_size}")
            for n_filters in ((32,64,128),(32,64, 64),(32,32,64)):
                print(f"N filters: {n_filters}")
                for dropout in (True, False):
                    print(f"Dropout: {dropout}")
                    for sepconv in (True, False):
                        print(f"Sepconv: {sepconv}")
                        run += 1
                        print(f"Run: {run}")
                        if run <= 74: continue

                        valaccuracy_by_fold = []
                        valloss_by_fold = []

                        for fold in range(4):
                            print(f"FOLD {fold}")
                            (train_x, train_y), (test_x, test_y) = dataseries.get_train_test_data(reverse=True, fold_num=fold)

                            seq_length = train_x.shape[1]
                            input_channels = train_x.shape[2]
                            model = Dynamic_CNN_categorical(sequence_length=seq_length, input_channels=input_channels,
                                                n_classes=3, conv_layers=conv_layers, kernel_size=kernel_size,
                                                n_filters=n_filters, dropout=dropout, sepconv=sepconv)

                            results = model.train(train_x, train_y, epochs=20, batch_size=32, tensorboard_modelname="MLP",
                                                  validation_data=(test_x, test_y))

                            valaccuracy_by_fold.append(results.history['val_acc'])
                            valloss_by_fold.append(results.history['val_loss'])

                            del model

                        valaccuracy_by_fold = np.stack(valaccuracy_by_fold)
                        valloss_by_fold = np.stack(valloss_by_fold)

                        acc = np.max(np.mean(valaccuracy_by_fold, axis=0))
                        result_table.append([conv_layers,kernel_size,n_filters,dropout,sepconv,acc])
                        print(pd.DataFrame(result_table, columns=['conv_layers','kernel_size','n_filters','dropout','sepconv','accuracy']))

                        # print(f"Brute force: {np.mean(brute_force_by_fold)} ({brute_force_by_fold})")
                        # print(
                        #     f"Accuracy: {acc} (EPOCH: {np.argmax(np.mean(valaccuracy_by_fold, axis=0))})")

    result_table = pd.DataFrame(result_table, columns=['conv_layers','kernel_size','n_filters','dropout','sepconv','accuracy'])
    result_table.to_csv("out.csv")