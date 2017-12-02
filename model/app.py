#!flask/bin/python
import numpy as np
from flask import Flask, jsonify
from keras.models import load_model
from util import *
# app = Flask(__name__)

regression_model = load_model('ff5_0.890613427055small.h5')

# @app.route('/')
# def index():
#     return "Hello, World!"

# @app.route('/api/premiums', methods=['POST'])
# def get_premiums():
#     if not request.json:
#         abort(400)
#     feature_vec = process_json(request.json)
#     vals = regression_model.predict(feature_vec)
#     plans = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
#     data = {plans[i]: vals[i] for i in xrange(len(plans))}
#     return jsonify(data)

# @app.route('/api/recommendation', methods=['POST'])
# def get_premiums():
#     if not request.json:
#         abort(400)
#     feature_vec = process_json(request.json)
#     vals = regression_model.predict(feature_vec)
#     denorm_vals = denorm_vals(list(regression_model.predict(vec)[0]))   
#     plans = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
#     data = {plans[i]: denorm_vals[i] for i in xrange(len(plans))}
#     return jsonify(data)


if __name__ == '__main__':
    # app.run(debug=True)
    pass