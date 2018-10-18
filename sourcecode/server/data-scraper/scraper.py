import sys, os, json, urllib
from collections import OrderedDict

"""
	Steamspy & steam web api scraper
	By Alex McGill
	Last Modified: 03/10/2018

	Usage:
	python scraper.py -f <filename.json>
"""


def get_args():
	loc = ""	
	for index, item in enumerate(sys.argv, start=1):
		if len(sys.argv) > index and sys.argv[index] == "-f":
			loc = sys.argv[index+1]
			print loc
			return loc
	print "Usage Error: 'python scraper.py -f <filename.json>'"
	print "--------------------"
	exit()


def get_json_file():
	filename = os.path.join(os.getcwd(), get_args())
	with open(filename) as data:
		apps = json.load(data, object_pairs_hook=OrderedDict)
		print "Loaded: ", filename
		return apps
	print "Error: Failed to load JSON file"
	print "--------------------"
	exit()


def get_game_ids(apps):
	ids = []
	print "%6s %1s" % ("appid", "name")
	for key, value in apps.items():
		print "%6s %1s" % (value["appid"],value["name"])
		ids.append(value["appid"])
	return ids


def get_steam_api_data(ids):
	count = 0
	collection = []
	directory = os.path.join(os.getcwd(), 'games/')
	if not os.path.exists(directory):
		os.makedirs(directory)
	for current in ids:
		count += 1	
		url ="https://store.steampowered.com/api/appdetails?appids=" + str(current) + "&cc=gb&l=en"
		print count, " | ", url
		# Steam API limits may occur
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		name = directory + str(current) + ".json"
		with open(name, 'w') as outfile:
			json.dump(data, outfile, indent=1)
	print "All files successfuly retrieved"

# Run Program
print "--------------------"

apps = get_game_ids(get_json_file())
get_steam_api_data(apps)

print "--------------------"

