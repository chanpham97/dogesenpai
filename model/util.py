import csv
import numpy as np
from keras.utils.np_utils import to_categorical


label_fields = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'PURCHASED']
fields = ['DOB', 'OPTIONAL_INSURED', 'WEIGHT', 'HEIGHT', 'BMI', 'PEOPLE_COVERED', 'ANNUAL_INCOME', 'longitude', 'latitude', 'sex', 'MARITAL_STATUS', 'E11.65', 'N18.9', 'R00.8', 'T85.622', 'B20.1', 'R19.7', 'R00.0', 'F10.121', 'G30.0', 'G80.4', 'R04.2', 'S62.308', 'M05.10', 'F14.121', 'G47.33', 'T84.011', 'Z91.010', 'B18.1']
# print fields[14]

def get_data_from_csv(fname='../norm_data.csv'):
    '''iterator over csv'''
    with open(fname) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def load_feature_vectors(fname='../norm_data.csv', wanted_labels=['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'PURCHASED']):
    vecs = []
    label_data = {label: [] for label in wanted_labels}
    count = 0
    for data in get_data_from_csv(fname=fname):
        count += 1
        if count > 1000000:
            break

        for label in wanted_labels:
            label_data[label].append(float(data[label]))

        for key in wanted_labels:
            del data[key]
        vec = np.array([float(data[key]) for key in fields])
        vecs.append(vec)

    return vecs, label_data


def get_feature_sets_regression(fname='../norm_data.csv'):
    wanted_labels=['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    vecs = []
    label_data = []
    count = 0
    for data in get_data_from_csv(fname=fname):
        count += 1
        # if count > 60000:
        #     break
        label_vec = []
        for label in wanted_labels:
            label_vec.append(float(data[label]))
        label_data.append(label_vec)

        for key in wanted_labels:
            del data[key]
        vec = np.array([float(data[key]) for key in fields])
        vecs.append(vec)
    X = np.array(vecs[:1000000])
    y = np.array(label_data[:1000000])
    X2 = np.array(vecs[1000000:])
    y2 = np.array(label_data[1000000:])

    return X, y, X2, y2

def get_feature_sets_classification(fname='../norm_datahot.csv', nn=True):
    vecs = []
    label_data = []
    label = 'PURCHASED'
    count = 0
    for data in get_data_from_csv(fname=fname):
        # count += 1
        # if count > 15000:
        #     break
        # ind = int(data[label])
        label_data.append(int(data[label]))
        # label_data.append([0 if i != ind else 1 for i in xrange(4)])
        del data[label]
        vec = np.array([float(data[key]) for key in fields])
        vecs.append(vec)

    if nn:
        label_data = to_categorical(label_data, num_classes=4)

    X = np.array(vecs[:1000000])
    y = np.array(label_data[:1000000])
    X2 = np.array(vecs[1000000:])
    y2 = np.array(label_data[1000000:])

    return X, y, X2, y2

def convert_to_value(reg_val, key):
    info = {'PLATINUM': (110.0, 406.0), 'OPTIONAL_INSURED': (500000.0, 1000000.0), 'ANNUAL_INCOME': (100000.0, 1000000.0), 'GOLD': (70.0, 286.0), 'WEIGHT': (100.0, 300.0), 'DOB': (-1014428902.0, 942099098.0), 'longitude': (-177.0, 171.0), 'HEIGHT': (50.0, 80.0), 'PEOPLE_COVERED': (1.0, 4.0), 'latitude': (7.0, 71.0), 'SILVER': (40.0, 196.0), 'BRONZE': (20.0, 136.0)}
    minny, maxy = info[key]
    middle = (minny+maxy)/2
    return reg_val*(maxy-middle)+middle

def denorm_vals(vals):
    labels = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    result = []
    for i in xrange(len(labels)):
        result.append(convert_to_value(vals[i], labels[i]))
    return result

