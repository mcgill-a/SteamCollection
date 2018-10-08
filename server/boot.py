from collections import OrderedDict
from flask import Flask, render_template, url_for, jsonify, abort
from flask_bootstrap import Bootstrap
import os, json, random
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.errorhandler(Exception)
def all_exception_handler(error):
	return 'Error', 500

@app.route('/test/<input>')
def test(input=None):
	data = {'input': input}
	return render_template('index.html', data=data)

@app.route('/games/')
def games():
	games = load_games()
	return render_template('games.html', games=games)


@app.route('/display/')
def display():
	filename = os.path.join(app.static_folder, 'data/ss-top100forever.json')
	with open(filename) as data:
		info = json.load(data, object_pairs_hook=OrderedDict)
		return render_template('display-all.html', info=info)
	return "Failed to json load data"

@app.route('/game/')
@app.route('/game/<appid>')
def game(appid=None):
	if (appid is not None):
		filename = "data/steam-api/" + appid + ".json"
		full_path = os.path.join(app.static_folder, filename)
        if (os.path.exists(str(full_path))):
			with open(full_path) as data:
				game = json.load(data)
				return render_template('game.html', game=game)
	return render_template('game.html', app=None)
	
def load_games():
	files = []
	count = 0
	directory = "data/steam-api/"
	full_path = os.path.join(app.static_folder, directory)
	for filename in os.listdir(full_path):
		if filename.endswith(".json") and count < 100:
			file_path = (full_path + filename)
			with open(file_path) as data:
				info = json.load(data)
				name = os.path.splitext(os.path.basename(file_path))[0]
				if info[name]["success"] == True:
					files.append(info)
					count += 1
	print "INFO: Game List Loaded | Count: " + str(count)
	random.shuffle(files)
	return files	

@app.route('/category/<category>')
def category(category=None):
	if (category is not None):
		games = load_games()
		render_template('games.html', games=games)
		

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
