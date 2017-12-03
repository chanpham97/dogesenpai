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
    counts = [0., 0.]
    for row in read_data('../unnorm_data.csv'):
        ind = int(row['G30.0'])
        counts[ind] += 1
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/counts[0], data[0])
    data[1] = map(lambda x: x/counts[1], data[1])

    with open('../json/alzheimers.json', 'w') as f:
        json.dump(data, f)


def num_covered_prem():
    data = [[0., 0., 0., 0.] for i in xrange(4)]
    counts = [0., 0., 0., 0.]
    for row in read_data('../data_wo_precon.csv'):        
        ind = int(row['PEOPLE_COVERED'])-1
        counts[ind] += 1
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/counts[0], data[0])
    data[1] = map(lambda x: x/counts[1], data[1])
    data[2] = map(lambda x: x/counts[2], data[2])
    data[3] = map(lambda x: x/counts[3], data[3])

    print data
    with open('../json/num_covered_prem.json', 'w') as f:
        json.dump(data, f)


def smoking_prem():
    data = [[0., 0., 0., 0.], [0., 0., 0., 0.]]
    counts = [0., 0.]
    for row in read_data('../unnorm_data.csv'):
        ind = int(row['TOBACCO'])
        counts[ind] += 1
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            data[ind][i] += float(row[label])

    data[0] = map(lambda x: x/counts[0], data[0])
    data[1] = map(lambda x: x/counts[1], data[1])

    with open('../json/smoking_prem.json', 'w') as f:
        json.dump(data, f)


def state_age():
    states = {}
    for row in read_data('../data_wo_precon.csv'):
        if row['DOB'] == '':
            continue
        birth = parser.parse(row['DOB']).replace(tzinfo=None)
        age = relativedelta(datetime.now(), birth).years
        state = row['state']
        if not state in states:
            states[state] = [float(age), 1.]
        else:
            states[state][0] += age
            states[state][1] += 1

    states = {state: v[0]/v[1] for state, v in states.iteritems()}

    print states
    with open('../json/state_age.json', 'w') as f:
        json.dump(states, f)


def prem_by_state():
    states = {}
    for row in read_data('../data_wo_precon.csv'):
        state = row['state']
        nums = []
        for i, label in enumerate(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']):
            nums.append(float(row[label]))
        if not state in states:
            states[state] = nums + [1.]
        else:
            for i in xrange(len(nums)):
                states[state][i] += nums[i]
            states[state][-1] += 1

    states = {
        'bronze': {state: v[0]/v[-1] for state, v in states.iteritems()},
        'silver': {state: v[1]/v[-1] for state, v in states.iteritems()},
        'gold': {state: v[2]/v[-1] for state, v in states.iteritems()},
        'platinum': {state: v[3]/v[-1] for state, v in states.iteritems()}
    }

    print states
    with open('../json/state_prem.json', 'w') as f:
        json.dump(states, f)


if __name__ == '__main__':
    with open('../json/num_covered_prem.json') as f:
        data = json.load(f)
        results = {i: data[i] for i in xrange(len(data))}
        results['labels'] = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    with open('../json/num_covered_prem.json', 'w') as f:
        json.dump(results, f)


        