from collections import OrderedDict
from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_bootstrap import Bootstrap
import ConfigParser, logging, os, json, random, re, string, time
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index(discover=None):
	return render_template('index.html')


@app.errorhandler(404)
def error_400(e):
	previous = request.referrer
	return render_template('error.html', error=404, previous=previous), 404


@app.errorhandler(500)
def error_500(e):
	previous = request.referrer
	return render_template('error.html', error=500, previous=previous), 500


#@app.route('/games/')
def games():
	games = load_games()
	random.shuffle(games)
	return render_template('games.html', games=games)

#@app.route('/search/')
@app.route('/games/')
def search():
	args = request.args.to_dict()
	filtered = {}
	for key, value in args.iteritems():
		if value:
			filtered[key] = value
	matched = lookup(filtered)
	if len(filtered) > 0 and len(matched) > 0:
		return render_template('search.html', games=matched, empty_search=False)
	else:
		# Use normal game load method as it processes data faster than lookup (search method)
		matched = load_games()
		return render_template('search.html', games=matched, empty_search=True)


def remove_html_tags(input):
	expr = re.compile('<.*?>')
	cleaned = re.sub(expr, '', input)
	return cleaned


@app.route('/games/<appid>')
def game(appid=None):
	desc = ""
	game_name = ""
	if (appid is not None):
		filename = "data/steam-api/" + appid + ".json"
		full_path = os.path.join(app.static_folder, filename)
		if (os.path.exists(str(full_path))):
			with open(full_path) as data:
				game = json.load(data)
				game_name = game[appid]["data"]["name"]
				# If there is a short decription then use it instead of longer description
				if len(game[appid]["data"]["short_description"]) > 40:
					desc = remove_html_tags(game[appid]["data"]["short_description"])[:300]
				else:
					desc = remove_html_tags(game[appid]["data"]["about_the_game"])[:300]
					# Get all complete sentences from the description
					desc = desc.rsplit('.', 1)[0] + "."
				return render_template('game.html', game=game, game_name=game_name,  desc=desc)
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
	return games


def load_genres():
	games = load_games()
	genres = []
	for index, game in enumerate(games):
		appid = next(iter(games[index]))
		if "genres" in game[str(appid)]["data"]:
			for genre in game[str(appid)]["data"]["genres"]:
				if genre["description"] not in genres:
					genres.append(genre["description"])
	return genres


def load_categories():
	games = load_games()
	categories = []
	for index, game in enumerate(games):
		appid = next(iter(games[index]))
		if "categories" in game[str(appid)]["data"]:
			for category in game[str(appid)]["data"]["categories"]:
				if category["description"] not in categories:
					categories.append(category["description"])
	return categories


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
				name = next(iter(info))
				if info[name]["success"] == True:
					for current in info[name]["data"]["developers"]:
						if current.lower() == dev.lower():
							games.append(info)
							count += 1
	return games


@app.route('/genres/<genre>')
@app.route('/genres/')
def genre(genre=None):
	if (genre is not None):
		actual_name = ""
		found = False
		games = load_genre_games(genre)
		for index, game, in enumerate(games):
			name = next(iter(games[index]))
			for current in game[name]["data"]["genres"]:
				if current["description"].lower() == genre.lower():
					found = True
					actual_name = current["description"]
					break
				if found:
					break
		return render_template('genre.html', games=games, genre=actual_name)
	else:
		genres = get_genre_info()
		return render_template('genres.html', genres=genres)


@app.route('/developers/<dev>')
def developer(dev=None):
	if dev is not None:
		actual_name = ""
		found = False
		games = load_developer_games(dev)
		for index, game in enumerate(games):
			name = next(iter(games[index]))
			for current in game[name]["data"]["developers"]:
				if dev.lower() == current.lower():
					found = True
					actual_name = current
					break
			if found:
				break
	if found:
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

def get_genre_info():
	data = {}
	games = load_games()
	for index, game in enumerate(games):
		appid = next(iter(games[index]))
		if "genres" in game[str(appid)]["data"]:
			for genre in game[str(appid)]["data"]["genres"]:
				name = genre["description"]
				if name in data:
					data[name] += 1
				else:
					data[name] = 1
	return data

def get_category_info():
	data = {}
	games = load_games()
	for index, game in enumerate(games):
		appid = next(iter(games[index]))
		if "categories" in game[str(appid)]["data"]:
			for category in game[str(appid)]["data"]["categories"]:
				name = category["description"]
				if name in data:
					data[name] += 1
				else:
					data[name] = 1
	return data


@app.route('/categories/<cat>')
@app.route('/categories/')
def category(cat=None):
	if cat is not None:
		actual_name = ""
		found = False
		games = load_category_games(cat)
		for index, game, in enumerate(games):
			name = next(iter(games[index]))
			for current in game[name]["data"]["categories"]:
				if current["description"].lower() == cat.lower():
					found = True
					actual_name = current["description"]
					break
				if found:
					break
		return render_template('category.html', games=games, category=actual_name)
	else:
		categories = get_category_info()
		return render_template('categories.html', categories=categories)


def lookup(args):
	query = {}
	for key, value in args.iteritems():
		if value:
			query[key.lower()] = value
	matched = []
	games = load_games()
	for index, game in enumerate(games):
		valid = True
		appid = next(iter(games[index]))
		for key, value in query.iteritems():
			value = value.lower()
			if key == "appid":
				if value != appid:
					valid = False
					break
			elif key == "name":
				if value not in game[str(appid)]["data"]["name"].lower():
					valid = False
					break
			elif key == "developer":
				devFound = False
				for dev in game[str(appid)]["data"]["developers"]:
					if value in dev.lower():
						devFound = True
				if devFound == False:
					valid = False
					break
			elif key == "genre":
				genreFound = False
				if "genres" in game[str(appid)]["data"]:
					for genre in game[str(appid)]["data"]["genres"]:
						if value in genre["description"].lower():
							genreFound = True
				if genreFound == False:
					valid = False
					break
			elif key == "category":
				categoryFound = False
				for category in game[str(appid)]["data"]["categories"]:
					categoryFound == False
					if value in category["description"].lower():
						categoryFound = True
				if categoryFound == False:
						valid = False
						break
			else:
				valid = False
		if valid:
			matched.append(game)
	return matched


@app.route('/api/')
def api():
	return render_template('api.html')


@app.route('/api/request/')
def api_search():
	args = request.args.to_dict()
	matched = lookup(args)
	ts = time.gmtime()
	output = (time.strftime("%Y-%m-%d %H:%M:%S", ts)) + " | " + \
            request.remote_addr + " | " + str(request.query_string)
	app.logger.info(output)
	if len(matched) > 0:
		return jsonify(matched)
	else:
		return jsonify('null')


@app.route('/api/games/<appid>')
def api_game(appid=None):
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
					desc = desc.rsplit('.', 1)[0] + "."
			return jsonify(game)
		else:
			output = {appid: ({'success': False})}
			return jsonify(output)
	else:
		return jsonify('null')


def init(app):
	config = ConfigParser.ConfigParser()
	try:
		config_location = "etc/defaults.cfg"
		config.read(config_location)

		app.config['DEBUG'] = config.get("config", "DEBUG")
		app.config['ip_address'] = config.get("config", "IP_ADDRESS")
		app.config['port'] = config.get("config", "PORT")
		app.config['url'] = config.get("config", "URL")

		app.config['log_location'] = config.get("logging", "LOCATION")
		app.config['log_file'] = config.get("logging", "NAME")
		app.config['log_level'] = config.get("logging", "LEVEL")
	except:
		print ("Could not read configs from: ", config_location)


def logs(app):
	log_pathname = app.config['log_location'] + app.config['log_file']
	file_handler = RotatingFileHandler(
		log_pathname, maxBytes=(1024 * 1024 * 10), backupCount=1024)
	file_handler.setLevel(app.config['log_level'])
	formatter = logging.Formatter(
		"%(levelname)s | %(module)s | %(funcName)s | %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.setLevel(app.config['log_level'])
	app.logger.addHandler(file_handler)


if __name__ == '__main__':
	init(app)
	logs(app)
	app.run(
		host=app.config['ip_address'],
		port=int(app.config['port']))
else:
	init(app)
	logs(app)
