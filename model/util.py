import csv
import datetime
import numpy as np
from geopy.geocoders import Nominatim
from dateutil import parser
from keras.utils.np_utils import to_categorical


label_fields = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'PURCHASED']
fields = ['DOB', 'OPTIONAL_INSURED', 'WEIGHT', 'HEIGHT', 'BMI', 'TOBACCO', 'PEOPLE_COVERED', 'ANNUAL_INCOME', 'longitude', 'latitude', 'sex', 'MARITAL_STATUS', 'E11.65', 'N18.9', 'R00.8', 'T85.622', 'B20.1', 'R19.7', 'R00.0', 'F10.121', 'G30.0', 'G80.4', 'R04.2', 'S62.308', 'M05.10', 'F14.121', 'G47.33', 'T84.011', 'Z91.010', 'B18.1']
print fields[-8]

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


def get_feature_sets_regression(fname='../norm_datahot.csv'):
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
    info = {'PLATINUM': (110.0, 406.0), 'OPTIONAL_INSURED': (500000.0, 1000000.0), 'ANNUAL_INCOME': (100000.0, 1000000.0), 'GOLD': (70.0, 286.0), 'WEIGHT': (100.0, 300.0), 'DOB': (-1014428902.0, 942099098.0), 'BMI': (2.4109954185755935, 18.01123829344433), 'longitude': (-177.0, 171.0), 'HEIGHT': (50.0, 80.0), 'PEOPLE_COVERED': (1.0, 4.0), 'latitude': (7.0, 71.0), 'SILVER': (40.0, 196.0), 'BRONZE': (20.0, 136.0)}
    minny, maxy = info[key]
    middle = (minny+maxy)/2
    return reg_val*(maxy-middle)+middle

def denormalize_vals(vals):
    labels = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    result = []
    for i in xrange(len(labels)):
        result.append(convert_to_value(vals[i], labels[i]))
    return result

def time_to_float(value):
    t = parser.parse(value).replace(tzinfo=None)
    return (t-datetime.datetime(1970,1,1)).total_seconds()

def to_lat_long(city, state):
    geolocator = Nominatim()
    location = geolocator.geocode("{}, {}".format(city, state))
    return (location.latitude, location.longitude)


def process_json(data):
    vec = []
    to_write = {}

    mm_dict = {'OPTIONAL_INSURED': (500000.0, 1000000.0), 'ANNUAL_INCOME': (100000.0, 1000000.0), 'WEIGHT': (100.0, 300.0), 'DOB': (-1014428902.0, 942099098.0), 'BMI': (2.4109954185755935, 18.01123829344433), 'longitude': (-177.0, 171.0), 'HEIGHT': (50.0, 80.0), 'PEOPLE_COVERED': (1.0, 4.0), 'latitude': (7.0, 71.0)}
    prec = {'E11.65': 'Type 2 diabetes mellitus with hyperglycemia', 'N18.9': 'Chronic kidney disease, unspecified.', 'Z91.010': 'Peanut Allergy', 'R00.8': 'Other abnormalities of heart beat', 'B20.1': 'HIV disease resulting in other bacterial infections', 'R19.7': 'Diarrhea, unspecified', 'R00.0': 'Tachycardia, unspecified', 'F10.121': 'Alcohol abuse with intoxication delirium', 'G30.0': 'Alzheimer\xe2\x80\x99s disease  with early onset', 'G80.4': 'Ataxic cerebral palsy', 'R04.2': 'cough with hemorrhage', 'S62.308': 'Unspecified fracture of specified metacarpal bone with unspecified laterality', 'M05.10': 'Rheumatoid lung disease with rheumatoid arthritis of unspecified site', 'F14.121': 'Cocaine Abuse with intoxicatiuon delirium', 'G47.33': 'Obstructive Sleep Apnea', 'T84.011': 'Broken internal left hip prosthesis, initial encounter', 'T85.622': 'Displacement of permanent\xc2\xa0sutures, initial encounter', 'B18.1': 'Chronic viral hepatitis B without delta-agent'}

    lat, lng = to_lat_long(data['city'], data['state'])
    data['latitude'] = lat
    data['longitude'] = lng

    for field, (minny, maxy) in mm_dict.iteritems():
        if field == 'BMI':
            continue
        value = data[field]
        if field == 'DOB':
            value = time_to_float(value)
        else:
            value = float(value)
        middle = (minny+maxy)/2.
        value = (value-middle)/(maxy-middle)
        to_write[field] = value
    h_squared = (convert_to_value(float(data['HEIGHT'])*2-1, 'HEIGHT')*0.025)**2
    w = convert_to_value(float(data['WEIGHT'])*2-1, 'WEIGHT')*0.45
    bmi = w/h_squared
    (minny, maxy) = mm_dict['BMI']
    middle = (minny+maxy)/2.
    value = (bmi-middle)/(maxy-middle)
    to_write['BMI'] = value
    to_write['TOBACCO'] = 1 if data['TOBACCO'] else 0
    to_write['sex'] = 1 if data['sex'] == 'M' else 0
    to_write['MARITAL_STATUS'] = 1 if data['MARITAL_STATUS'] == 'M' else 0

    for p in prec:
        to_write[p] = 1 if data[p] else 0

    for field in fields:
        vec.append(to_write[field])
    return np.array([vec])


if __name__ == '__main__':
    ex = {
        "DOB": "1980-02-08",
        "OPTIONAL_INSURED": 500000,
        "WEIGHT": 150,
        "HEIGHT": 70,
        "PEOPLE_COVERED": 3,
        "ANNUAL_INCOME": 100000,
        "longitude": 100,
        "latitude": 70,
        "sex": "M",
        "MARITAL_STATUS": "S",
        "TOBACCO": True,
        "E11.65": True,
        "N18.9": False,
        "R00.8": False,
        "T85.622": False,
        "B20.1": False,
        "R19.7": True,
        "R00.0": False,
        "F10.121": False,
        "G30.0": False,
        "G80.4": False,
        "R04.2": False,
        "S62.308": False,
        "M05.10": False,
        "F14.121": False,
        "G47.33": False,
        "T84.011": False,
        "Z91.010": False,
        "B18.1": False
    }
    print process_json(ex)
