#!flask/bin/python
import numpy as np
from flask import Flask, jsonify
from keras.models import load_model
from util import *
app = Flask(__name__)

regression_model = load_model('regression1.h5')

@app.route('/')
def hello():
    return jsonify({'data': 'hello'})

@app.route('/premium', methods=['POST'])
def get_premiums():
    if not request.json:
        abort(400)
    feature_vec = process_json(request.json)
    vals = regression_model.predict(feature_vec)
    denorm_vals = denorm_vals(list(vals[0]))   
    plans = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    data = {plans[i]: denorm_vals[i] for i in xrange(len(plans))}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
    # import time
    # start = time.time()
    # ex = {
    #     'DOB': '1980-02-08',
    #     'OPTIONAL_INSURED': 500000,
    #     'WEIGHT': 150,
    #     'HEIGHT': 70,
    #     'BMI': 30,
    #     'PEOPLE_COVERED': 3,
    #     'ANNUAL_INCOME': 100000,
    #     'longitude': 100,
    #     'latitude': 70,
    #     'sex': 'M',
    #     'MARITAL_STATUS': 'S',
    #     'E11.65': True,
    #     'N18.9': False,
    #     'R00.8': False,
    #     'T85.622': False,
    #     'B20.1': False,
    #     'R19.7': True,
    #     'R00.0': False,
    #     'F10.121': False,
    #     'G30.0': False,
    #     'G80.4': False,
    #     'R04.2': False,
    #     'S62.308': False,
    #     'M05.10': False,
    #     'F14.121': False,
    #     'G47.33': False,
    #     'T84.011': False,
    #     'Z91.010': False,
    #     'B18.1': False
    # }
    # feature_vec = process_json(ex)
    # vals = regression_model.predict(feature_vec)
    # denorm_vals = denorm_vals(list(vals[0]))  
    # plans = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    # data = {plans[i]: denorm_vals[i] for i in xrange(len(plans))}
    # print data, time.time()-start
