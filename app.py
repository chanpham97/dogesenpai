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

@app.route('/doge')
def doge_hello():
	return render_template('index-doge.html')
