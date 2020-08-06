from __future__ import print_function
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn import preprocessing

import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Reshape, GlobalAveragePooling1D
from keras.layers import Conv2D, MaxPooling2D, Conv1D, MaxPooling1D
from keras.utils import np_utils


def feature_normalize_d(dataset):

    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    max_d = np.max(dataset, axis=0)
    min_d = np.min(dataset, axis=0)
    for i in range(0, dataset.shape[1]):
        if sigma[i] == 0:
            sigma[i] = 1
    return (dataset - min_d)/(max_d - min_d)


def feature_normalize_r(dataset):

    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    max_d = np.max(dataset, axis=0)
    min_d = np.min(dataset, axis=0)
    for i in range(0, dataset.shape[1]):
        if sigma[i] == 0:
            sigma[i] = 1
    return (dataset - min_d)/(max_d - min_d)


def read_data(file_path):
    df = pd.read_csv(file_path)
    return df


LABELS = ["line", "shake", "square", "circle"]
DIS = ["50", "100", "150"]
ANG = ["0", "30", "60"]
result = [0, 0, 0, 0]
resultN = [0, 0, 0, 0]
mACC = [0, 0, 0, 0]
ACC = 0
outputN = 5
face = 0

model = load_model('./bestmodel/C4_30_10_90r_0r432_3.h5')

for ang in range(0, 3):
    result = [0, 0, 0, 0]
    for dis in range(0, 3):
        result = [0, 0, 0, 0]
        for lab in range(0, 4):
            print(LABELS[lab])
            result = [0, 0, 0, 0]
            for j in range(1, 21):
                #phase = read_data('../reader_data/ML_realdata/phase_still_0_50_' + str(j) + '.csv')
                rssi = read_data('../reader_data/ML_realdata/rssi_' + LABELS[lab] + '_' + ANG[ang] + '_' + DIS[dis] + '_' + str(
                    face) + '_' + str(outputN) + '_' + str(j) + '.csv')
                distance = read_data('../reader_data/ML_realdata/distance_' + LABELS[lab] + '_' + ANG[ang] + '_' + DIS[dis] + '_' + str(
                    face) + '_' + str(outputN) + '_' + str(j) + '.csv')

                X_distance = np.asarray(distance, dtype=np.float32)
                X_rssi = np.asarray(rssi, dtype=np.float32)

                X_distance = feature_normalize_d(X_distance)
                X_rssi = feature_normalize_r(X_rssi)

                size = X_rssi.shape[1]

                X_test_A = []
                for i in range(0, size):
                    A = np.hstack(
                        (X_distance[:, i][:, np.newaxis], X_rssi[:, i][:, np.newaxis]))
                    if i == 0:
                        X_test_A = A
                    else:
                        X_test_A = np.concatenate((X_test_A, A))
                X_test = np.asarray(np.vsplit(X_test_A, size))

                # Set input & output dimensions
                num_time_periods, num_sensors = X_test.shape[1], X_test.shape[2]
                num_classes = 4

                # Set input_shape / reshape for Keras
                # Remark: acceleration data is concatenated in one array in order to feed
                # it properly into coreml later, the preferred matrix of shape [40,3]
                # cannot be read in with the current version of coreml (see also reshape
                # layer as the first layer in the keras model)
                input_shape = (num_time_periods*num_sensors)

                # print('input_shape:', input_shape)

                x_test = X_test

                x_test = x_test.reshape(x_test.shape[0], input_shape)

                x_test = x_test.astype("float32")
                # print('test after load: ', model.predict(x_test))
                y_pred_test = model.predict(x_test)
                # Take the class with the highest probability from the test predictions
                max_y_pred_test = np.argmax(y_pred_test, axis=1)
                resultN = [0, 0, 0, 0]
                for i in range(0, size):
                    # print(j,max_y_pred_test[i])
                    resultN[max_y_pred_test[i]
                            ] = resultN[max_y_pred_test[i]] + 1
                # print(resultN)
                # print(resultN.index(max(resultN)))
                result[resultN.index(max(resultN))
                       ] = result[resultN.index(max(resultN))] + 1

    # print(k+1)
            print(DIS[dis], ANG[ang])
            ACC = ACC + result[lab]
            mACC[lab] = mACC[lab] + result[lab]
            result[0] = round(result[0]/20.0, 3)
            result[1] = round(result[1]/20.0, 3)
            result[2] = round(result[2]/20.0, 3)
            result[3] = round(result[3]/20.0, 3)
            print(result)

print("Acc: ", ACC / 720.0)
print("line: ", mACC[0] / 180.0)
print("shake: ", mACC[1] / 180.0)
print("square: ", mACC[2] / 180.0)
print("circle: ", mACC[3] / 180.0)
