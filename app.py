from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from keras.models import load_model
from model.util import *

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app

regression_model = load_model('regression1.h5')
app = create_app()

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/doge')
def doge_hello():
	return render_template('index-doge.html')


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
