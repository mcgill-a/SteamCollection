from collections import OrderedDict
from flask import Flask, render_template, url_for, jsonify
from flask_bootstrap import Bootstrap
import os, json, random, re
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test/<input>')
def test(input=None):
	data = {'input': input}
	return render_template('index.html', data=data)

@app.route('/games/')
def games():
	games = load_games()
	random.shuffle(games)
	return render_template('games.html', games=games)


@app.route('/display/')
def display():
	filename = os.path.join(app.static_folder, 'data/ss-top100forever.json')
	with open(filename) as data:
		info = json.load(data, object_pairs_hook=OrderedDict)
		return render_template('display-all.html', info=info)
	return "Failed to json load data"


def remove_html_tags(input):
	expr = re.compile('<.*?>')
	cleaned = re.sub(expr, '', input)
	return cleaned

@app.route('/game/')
@app.route('/game/<appid>')
def game(appid=None):
	desc = "";
	if (appid is not None):
		filename = "data/steam-api/" + appid + ".json"
		full_path = os.path.join(app.static_folder, filename)
        if (os.path.exists(str(full_path))):
			with open(full_path) as data:
				game = json.load(data)
				# If there is a short decription then use it instead of longer description
				if len(game[appid]["data"]["short_description"]) > 40:
					desc = remove_html_tags(game[appid]["data"]["short_description"])[:300]
				else:
					desc = remove_html_tags(game[appid]["data"]["about_the_game"])[:300]
				# Get all complete sentences from the description
				desc = desc.rsplit('.',1)[0] + "."
				return render_template('game.html', game=game, desc=desc)
	return render_template('game.html', app=None)
	
def load_games():
	games = []
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
					games.append(info)
					count += 1
	print "INFO: Game List Loaded | Count: " + str(count)
	return games

def load_developer_games(dev):
	games = []
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
					for current in info[name]["data"]["developers"]:
						if current.lower() == dev.lower():
							games.append(info)
							count += 1
	if count > 0:
		print "INFO: Developer Game List Loaded | " + dev + " | Count: " + str(count)
	return games


@app.route('/category/')
@app.route('/category/<category>')
def category(category=None):
	if (category is not None):
		return "Category | " + category
	else:
		return "Category"


@app.route('/developer/')
@app.route('/developer/<dev>')
def developer(dev=None):
	if dev is not None:
		games = load_developer_games(dev)
		return render_template('games.html', games=games)
	else:
		return "Developers"


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
