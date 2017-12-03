from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
	app = Flask(__name__)
	Bootstrap(app)
	return app

app = create_app()

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/d3')
def d3_test():
	return render_template('d3.html')

@app.route('/precondhot.csv')
def data():
	return send_from_directory('')