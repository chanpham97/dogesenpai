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
    min_max_fields = ['OPTIONAL_INSURED', 'WEIGHT', 'DOB', 'HEIGHT', 'PEOPLE_COVERED', 'SILVER', 'BRONZE', 'PLATINUM', 'ANNUAL_INCOME', 'longitude', 'latitude', 'GOLD', 'BMI']
    mm_dict = {field: (1000000000000000., -1000000000000000.) for field in min_max_fields}
    print 'Finding min/max for fields...'
    progress = 0
    for row in read_data(csv_file):
        progress += 1
        if row['DOB'] == '':
            continue
        for field, (minny, maxy) in mm_dict.iteritems():
            if field == 'BMI':
                continue
            value = row[field]
            if field == 'DOB':
                value = time_to_float(value)
            else:
                value = float(value)
            
            minny = min(minny, value)
            maxy = max(maxy, value)

            mm_dict[field] = (minny, maxy)

        # calculate BMI
        h_squared = (convert_to_value(float(row['HEIGHT'])*2-1, 'HEIGHT')*0.025)**2
        w = convert_to_value(float(row['WEIGHT'])*2-1, 'WEIGHT')*0.45
        bmi = w/h_squared
        (minny, maxy) = mm_dict['BMI']
        minny = min(minny, bmi)
        maxy = max(maxy, bmi)
        mm_dict['BMI'] = (minny, maxy)

        if progress % 50000 == 0:
            print progress

    print mm_dict
    quit()
    # other fields
    other_fields = ['sex', 'MARITAL_STATUS', 'PURCHASED', 'TOBACCO']

    '''
    sex - '',M,F (blank -> F)
    MARITAL_STATUS - S,M
    EMPLOYMENT_STATUS - Unemployed => skip
    PURCHASED - ['Bronze', 'Silver', 'Gold', 'Platinum']
    PRE_CONDITIONS - [0, 0.3, 0.6, 1.0] (none, low, med, high)
    TOBACCO - Yes/No -> 0
    '''
    field_names = min_max_fields + other_fields + preconditions.keys()

    print 'Transforming data...'
    outfile = 'norm_datahot.csv'
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
                if field == 'BMI':
                    continue
                value = row[field]
                if field == 'DOB':
                    value = time_to_float(value)
                else:
                    value = float(value)
                middle = (minny+maxy)/2.
                value = (value-middle)/(maxy-middle)
                to_write[field] = value

            # calculate BMI
            h_squared = (convert_to_value(float(row['HEIGHT'])*2-1, 'HEIGHT')*0.025)**2
            w = convert_to_value(float(row['WEIGHT'])*2-1, 'WEIGHT')*0.45
            bmi = w/h_squared
            (minny, maxy) = mm_dict['BMI']
            middle = (minny+maxy)/2.
            value = (bmi-middle)/(maxy-middle)
            to_write['BMI'] = value

            # other fields
            to_write['sex'] = 1 if row['sex'] == 'M' else 0
            to_write['MARITAL_STATUS'] = 1 if row['MARITAL_STATUS'] == 'M' else 0
            to_write['PURCHASED'] = ['Bronze', 'Silver', 'Gold', 'Platinum'].index(row['PURCHASED'])
            to_write['TOBACCO'] = 1 if row['TOBACCO'] == 'Yes' else 0

            # Handle Pre-Conditions
            leftover_pcs = set(preconditions.keys())
            if '[' in row['PRE_CONDITIONS']:
                pcs = eval(row['PRE_CONDITIONS'])

                for pc in pcs:
                    to_write[pc['ICD_CODE']] = 1#preconditions_value_map[pc['Risk_factor']]
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

def convert_to_value(reg_val, key):
    info = {'PLATINUM': (110.0, 406.0), 'OPTIONAL_INSURED': (500000.0, 1000000.0), 'ANNUAL_INCOME': (100000.0, 1000000.0), 'GOLD': (70.0, 286.0), 'WEIGHT': (100.0, 300.0), 'DOB': (-1014428902.0, 942099098.0), 'longitude': (-177.0, 171.0), 'HEIGHT': (50.0, 80.0), 'PEOPLE_COVERED': (1.0, 4.0), 'latitude': (7.0, 71.0), 'SILVER': (40.0, 196.0), 'BRONZE': (20.0, 136.0)}
    minny, maxy = info[key]
    middle = (minny+maxy)/2
    return reg_val*(maxy-middle)+middle



def lassoize(fname='norm_datahot.csv'):
    field_names = ['OPTIONAL_INSURED', 'WEIGHT', 'DOB', 'HEIGHT', 'BMI', 'PEOPLE_COVERED', 'SILVER', 'BRONZE', 'PLATINUM', 'ANNUAL_INCOME', 'longitude', 'latitude', 'GOLD', 'sex', 'MARITAL_STATUS', 'PURCHASED', 'TOBACCO', 'E11.65', 'N18.9', 'R00.8', 'T85.622', 'B20.1', 'R19.7', 'R00.0', 'F10.121', 'G30.0', 'G80.4', 'R04.2', 'S62.308', 'M05.10', 'F14.121', 'G47.33', 'T84.011', 'Z91.010', 'B18.1']
    min_max_fields = ['OPTIONAL_INSURED', 'WEIGHT', 'DOB', 'HEIGHT', 'BMI', 'PEOPLE_COVERED', 'SILVER', 'BRONZE', 'PLATINUM', 'ANNUAL_INCOME', 'longitude', 'latitude', 'GOLD']
    with open('lasso_datahot.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for row in read_data(fname):
            for field in min_max_fields:
                row[field] = (float(row[field])+1)/2.0
            row['DOB'] *= -1
            writer.writerow(row)


def calc_avs(fname='../../all_data.csv'):
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    fields = ['OPTIONAL_INSURED', 'WEIGHT', 'DOB', 'HEIGHT', 'PEOPLE_COVERED', 'SILVER', 'BRONZE', 'PLATINUM', 'ANNUAL_INCOME', 'longitude', 'latitude', 'GOLD', 'BMI']

    data = {tier: {field: 0. for field in fields} for tier in tiers}
    counts = {tier: 0. for tier in tiers}

    for row in read_data(fname):
        tier = row['PURCHASED']
        if row['state'] == 'Texas':
            continue
        try:
            data[tier]['DOB'] += time_to_float(row['DOB'])
        except:
            continue
        counts[tier] += 1
        for field in fields:
            if field in ['BMI', 'DOB']:
                continue
            data[tier][field] += float(row[field])

        h_squared = (convert_to_value(float(row['HEIGHT'])*2-1, 'HEIGHT')*0.025)**2
        w = convert_to_value(float(row['WEIGHT'])*2-1, 'WEIGHT')*0.45
        bmi = w/h_squared
        data[tier]['BMI'] += bmi

    print counts

    for tier in tiers:
        for field in fields:
            data[tier][field] /= counts[tier]

    print data


def preconditions_only(fname='../data_wo_precon.csv'):
    field_names = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'PURCHASED', 'state', 'latitude', 'longitude', 'TOBACCO', 'OPTIONAL_INSURED', 'ANNUAL_INCOME']
    preconditions = find_preconditions()
    preconditions_value_map = {'Low': 0.333, 'Medium': 0.666, 'High': 1}
    with open('precond.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names+preconditions.keys())
        writer.writeheader()
        for row in read_data(fname):
            data = {}
            for field in field_names:
                data[field] = row[field]
            # Handle Pre-Conditions
            leftover_pcs = set(preconditions.keys())
            if '[' in row['PRE_CONDITIONS']:
                pcs = eval(row['PRE_CONDITIONS'])

                for pc in pcs:
                    data[pc['ICD_CODE']] = preconditions_value_map[pc['Risk_factor']]
                    leftover_pcs.remove(pc['ICD_CODE'])

            for pc in leftover_pcs:
                data[pc] = 0
            writer.writerow(data)
            


if __name__ == '__main__':
    normalize_data()
    # lassoize()
    # print find_values('PURCHASED')
