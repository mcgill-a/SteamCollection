from collections import OrderedDict
from flask import Flask, render_template, url_for, jsonify
from flask_bootstrap import Bootstrap
import os, json, random, re, string
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


@app.route('/games/<appid>')
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

def load_genre_games(genre_input):
	games = load_games()
	relevant_games = []
	for index, game in enumerate(games):
		genres = []
		appid = next(iter(games[index]))
		if "genres" in game[str(appid)]["data"]:
			for genre in game[str(appid)]["data"]["genres"]:
				if genre_input.lower() == genre["description"].lower():
					relevant_games.append(game)
	return relevant_games

def load_category_games(cat_input):
	games = load_games()
	relevant_games = []
	for index, game in enumerate(games):
		genres = []
		appid = next(iter(games[index]))
		if "categories" in game[str(appid)]["data"]:
			for category in game[str(appid)]["data"]["categories"]:
				if cat_input.lower() == category["description"].lower():
					relevant_games.append(game)
	return relevant_games


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
				#name = os.path.splitext(os.path.basename(file_path))[0]
				name = next(iter(info))
				if info[name]["success"] == True:
					for current in info[name]["data"]["developers"]:
						if current.lower() == dev.lower():
							games.append(info)
							count += 1
	if count > 0:
		print "INFO: Developer Game List Loaded | " + dev + " | Count: " + str(count)
	return games


@app.route('/genres/<genre>')
def genre(genre=None):
	if (genre is not None):
		games = load_genre_games(genre)
		genre = string.capwords(genre)
		return render_template('genre.html', games=games, genre=genre)
	else:
		return render_template('genre.html', genre=genre)

@app.route('/genres/')
def genres():
	# List all genres
	return "genres"


@app.route('/developers/<dev>')
def developer(dev=None):
	if dev is not None:
		actual_name = "0"
		games = load_developer_games(dev)
		for index, game in enumerate(games):
			name = next(iter(games[index]))
			for current in game[name]["data"]["developers"]:
				if dev.lower() == current.lower():
					actual_name = current
					break;
			if actual_name != "0":
				break;
		dev = string.capwords(dev)
		return render_template('developer.html', games=games, developer=actual_name)
	else:
		return render_template('developer.html', developer=dev)

@app.route('/developers/')
def developers():
	devs = get_dev_info()
	return render_template('developers.html', devs=devs)


def get_dev_info():
	data = {}
	games = load_games()
	for index, game in enumerate(games):
		appid = next(iter(games[index]))
		for dev in game[str(appid)]["data"]["developers"]:
			if dev in data:
				data[dev] += 1
			else:
				data[dev] = 1
	return data

@app.route('/categories/<cat>')
def category(cat=None):
	if cat is not None:
		games = load_category_games(cat)
		cat = string.capwords(cat)
		return render_template('category.html', games=games, category=cat)
	else:
		return render_template('category.html', category=cat)

@app.route('/categories/')
def categories():
	# List all categories
	return "categories"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
