import csv
from datetime import datetime
import time
import json
from dateutil import parser
from vitech import read_data
from dateutil.relativedelta import relativedelta


def avg_age_prem():
    ages = {age: [0., 0., 0., 0., 0.] for age in xrange(111)}
    for row in read_data('../unnorm_data.csv'):
        birth = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row['DOB']))))
        
        age = relativedelta(datetime.now(), birth).years
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            ages[age][i] += float(row[label])

        ages[age][-1] += 1

    results = [[], [], [], [], []]
    for age in ages:
        if sum(ages[age]) == 0:
            continue
        count = ages[age][-1]
        ages[age] = map(lambda x: x/count, ages[age][:-1])
        for i, term in enumerate([age] + ages[age]):
            results[i].append(term)
    print results
    with open('../json/ageprem.json', 'w') as f:
        json.dump(results, f)


def alzheimers_prem():
    data = [[0., 0., 0., 0.], [0., 0., 0., 0.]]
    for row in read_data('../unnorm_data.csv'):
        ind = int(row['G30.0'])    
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/len(data[0]), data[0])
    data[1] = map(lambda x: x/len(data[1]), data[1])

    with open('../json/alzheimers.json', 'w') as f:
        json.dump(data, f)


def num_covered_prem():
    data = [[0., 0., 0., 0.] for i in xrange(4)]
    for row in read_data('../data_wo_precon.csv'):        
        ind = row['G30.0']
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/len(data[0]), data[0])
    data[1] = map(lambda x: x/len(data[1]), data[1])
    data[2] = map(lambda x: x/len(data[2]), data[2])
    data[3] = map(lambda x: x/len(data[3]), data[3])

    print results
    with open('../json/num_covered_prem.json', 'w') as f:
        json.dump(results, f)


def smoking_prem():
    data = [[0., 0., 0., 0.], [0., 0., 0., 0.]]
    for row in read_data('../unnorm_data.csv'):
        ind = int(row['TOBACCO'])    
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/len(data[0]), data[0])
    data[1] = map(lambda x: x/len(data[1]), data[1])

    print results
    with open('../json/alzheimers.json', 'w') as f:
        json.dump(data, f)


def state_age():
    pass


def prem_by_state():
    pass


if __name__ == '__main__':
    alzheimers_prem()
        