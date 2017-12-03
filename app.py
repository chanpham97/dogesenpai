from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from keras.models import load_model
from model.util import *
import json

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app

regression_model = load_model('regression1.h5')
app = create_app()

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/d3')
def d3_test():
	return render_template('d3.html')


@app.route('/api/ageprem')
def age_prem():
    with open('json/ageprem.json') as f:
        return jsonify(json.load(f))

@app.route('/api/alzheimers')
def alzheimers():
    with open('json/alzheimers.json') as f:
        return jsonify(json.load(f))

@app.route('/api/num-covered-prem')
def num_covered_prem():
    with open('json/num_covered_prem.json') as f:
        return jsonify(json.load(f))


@app.route('/api/premium', methods=['POST'])
def get_premiums():
    data = request.get_json(force=True)
    if not data:
        abort(400)
    feature_vec = process_json(data)
    vals = regression_model.predict(feature_vec)
    denorm_vals = denormalize_vals(list(vals[0]))   
    plans = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
    data = {plans[i]: denorm_vals[i] for i in xrange(len(plans))}
    return jsonify(data)
