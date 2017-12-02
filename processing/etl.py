# -*- coding: utf-8 -*-
import datetime
from vitech import *
from dateutil import parser


csv_file = '../all_data.csv'

def normalize_data():
    fields = 'OPTIONAL_INSURED,WEIGHT,DOB,MARITAL_STATUS,sex,email,PEOPLE_COVERED,address,collection_id,HEIGHT,,SILVER,BRONZE,PLATINUM,city,ANNUAL_INCOME,TOBACCO,EMPLOYMENT_STATUS,longitude,id,state,PURCHASED,latitude,GOLD,PRE_CONDITIONS'.split(',')
    preconditions = find_preconditions()
    preconditions_value_map = {'Low': 0.333, 'Medium': 0.666, 'High': 1}

    # need to find min/max for fields first
    min_max_fields = ['OPTIONAL_INSURED', 'WEIGHT', 'DOB', 'HEIGHT', 'PEOPLE_COVERED', 'SILVER', 'BRONZE', 'PLATINUM', 'ANNUAL_INCOME', 'longitude', 'latitude', 'GOLD']
    mm_dict = {field: (0., 0.) for field in min_max_fields}
    print 'Finding min/max for fields...'
    progress = 0
    for row in read_data(csv_file):
        progress += 1
        if row['DOB'] == '':
            continue
        for field, (minny, maxy) in mm_dict.iteritems():
            value = row[field]
            if field == 'DOB':
                value = time_to_float(value)
            else:
                value = float(value)
            
            minny = min(minny, value)
            maxy = max(maxy, value)

            mm_dict[field] = (minny, maxy)
        if progress % 50000 == 0:
            print progress
    # other fields
    other_fields = ['sex', 'MARITAL_STATUS', 'PURCHASED']
    '''
    sex - '',M,F (blank -> F)
    MARITAL_STATUS - S,M
    EMPLOYMENT_STATUS - Unemployed => skip
    PURCHASED - ['Platinum', 'Gold', 'Silver', 'Bronze']
    PRE_CONDITIONS - [0, 0.3, 0.6, 1.0] (none, low, med, high)
    '''
    field_names = min_max_fields + other_fields + preconditions.keys()

    print 'Transforming data...'
    outfile = 'norm_data.csv'
    progress = 0
    with open(outfile, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=list(field_names))
        writer.writeheader()
        for row in read_data(csv_file):
            progress += 1
            if progress % 50000 == 0:
                print progress
            to_write = {}
            if row['DOB'] == '':
                continue

            # normalizable fields
            for field, (minny, maxy) in mm_dict.iteritems():
                value = row[field]
                if field == 'DOB':
                    value = time_to_float(value)
                else:
                    value = float(value)
                middle = (minny+maxy)/2.
                value = (value-middle)/(maxy-middle)
                to_write[field] = value

            # other fields
            to_write['sex'] = 1 if row['sex'] == 'M' else 0
            to_write['MARITAL_STATUS'] = 1 if row['MARITAL_STATUS'] == 'M' else 0
            to_write['PURCHASED'] = ['Bronze', 'Silver', 'Gold', 'Platinum'].index(row['PURCHASED'])

            # Handle Pre-Conditions
            leftover_pcs = set(preconditions.keys())
            if '[' in row['PRE_CONDITIONS']:
                pcs = eval(row['PRE_CONDITIONS'])

                for pc in pcs:
                    to_write[pc['ICD_CODE']] = preconditions_value_map[pc['Risk_factor']]
                    leftover_pcs.remove(pc['ICD_CODE'])

            for pc in leftover_pcs:
                to_write[pc] = 0
            writer.writerow(to_write)




def find_preconditions():
    '''Gets all of the possible preconditions and stores them in a dict'''
    result = {'E11.65': 'Type 2 diabetes mellitus with hyperglycemia', 'N18.9': 'Chronic kidney disease, unspecified.', 'Z91.010': 'Peanut Allergy', 'R00.8': 'Other abnormalities of heart beat', 'B20.1': 'HIV disease resulting in other bacterial infections', 'R19.7': 'Diarrhea, unspecified', 'R00.0': 'Tachycardia, unspecified', 'F10.121': 'Alcohol abuse with intoxication delirium', 'G30.0': 'Alzheimer\xe2\x80\x99s disease  with early onset', 'G80.4': 'Ataxic cerebral palsy', 'R04.2': 'cough with hemorrhage', 'S62.308': 'Unspecified fracture of specified metacarpal bone with unspecified laterality', 'M05.10': 'Rheumatoid lung disease with rheumatoid arthritis of unspecified site', 'F14.121': 'Cocaine Abuse with intoxicatiuon delirium', 'G47.33': 'Obstructive Sleep Apnea', 'T84.011': 'Broken internal left hip prosthesis, initial encounter', 'T85.622': 'Displacement of permanent\xc2\xa0sutures, initial encounter', 'B18.1': 'Chronic viral hepatitis B without delta-agent'}
    # short circuit now that we have the result
    return result

    preconds = {}

    for data in read_data(csv_file):
        if '[' in data['PRE_CONDITIONS']:
            pcs = eval(data['PRE_CONDITIONS'])
            for pc in pcs:
                preconds[pc['ICD_CODE']] = pc['condition_name']
    return preconds

def find_values(field_name):
    vals = {}
    for row in read_data(csv_file):
        if row[field_name] in vals:
            vals[row[field_name]] += 1
        else:
            vals[row[field_name]] = 1
    return vals


def time_to_float(value):
    t = parser.parse(value).replace(tzinfo=None)
    return (t-datetime.datetime(1970,1,1)).total_seconds()

if __name__ == '__main__':
    normalize_data()
