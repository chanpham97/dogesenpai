# -*- coding: utf-8 -*-
import requests
import csv
import time
import sys


collections = ['v_quotes', 'v_participant', 'v_participant_detail', 'v_plan_detail']


def get_data_from_vitech(collection, rows=50, start=0):
    url = 'https://v3v10.vitechinc.com/solr/{}/select?indent=on&q=*:*&wt=json&rows={}&start={}'.format(collection, rows, start)
    return requests.get(url).json()


def log_collection(collection, rows=1482000):
    name = collection + '.txt'
    start = time.time()
    print 'querying from {}...'.format(collection)
    data = get_data_from_vitech(collection, rows=rows)
    print 'query took {}s'.format(time.time()-start)
    num_found = data['response']['numFound']
    log_data(data, name, first=True)


def log_data(data, name, first=False):
    docs = data['response']['docs']
    with open(name, 'a') as f:
        field_names = sorted(docs[0].keys())
        field_names = set(field_names)
        for doc in docs:
            field_names = field_names.union(doc.keys())
        writer = csv.DictWriter(f, fieldnames=list(field_names))
        if first:
            writer.writeheader()
        for doc in docs:
            data2 = {key: unicode(value).encode('utf-8') for key, value in doc.iteritems() if key in field_names}
            data2.update({key: '' for key in field_names if key not in doc.keys()})
            writer.writerow(data2)

def read_data(name):
    '''create iterator over data in csv'''
    with open(name) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def merge():
    info = {}
    field_names = set()
    for c in collections[:-1]:
        for data in read_data(c + '.txt'):
            field_names = field_names.union(set(data.keys()))

            if data['id'] in info:
                info[data['id']].update(data)
            else:
                info[data['id']] = data
    print field_names
    with open('all_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=list(field_names))
        writer.writeheader()
        for _, val in info.iteritems():
            # print val
            data2 = {key: value for key, value in val.iteritems() if key in field_names}
            data2.update({key: '' for key in field_names if key not in val.keys()})
            # print data2
            writer.writerow(data2)


if __name__ == '__main__':
    merge()
