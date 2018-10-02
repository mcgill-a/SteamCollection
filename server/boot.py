from flask import Flask, render_template, url_for, jsonify
from flask_bootstrap import Bootstrap
import os
import json
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test/<input>')
def test(input=None):
	data = {'input': input}
	return render_template('index.html', data=data)

@app.route('/display/')
def display():
	filename = os.path.join(app.static_folder, 'data/ss-top100forever.json')
	with open(filename) as data:
		stats = json.load(data)
		return jsonify(stats)
	return "Failed to load data"

@app.route('/send/', methods=['GET','POST'])
def send():
	return "Send JSON"	

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
