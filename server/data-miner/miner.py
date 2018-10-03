import sys, os, json, urllib
from collections import OrderedDict

"""
	Steamspy appid Miner
	by Alex McGill
	03/10/2018
"""
print "--------------------"
print "Miner Loaded"

def get_args():
	loc = ""	
	for index, item in enumerate(sys.argv, start=1):
		if sys.argv[index] == "-f" and len(sys.argv) > index:
			loc = sys.argv[index+1]
			print loc
			return loc
	print("Failed to get argument")
	return ""


def get_json_file():
	filename = os.path.join(os.getcwd(), get_args())
	with open(filename) as data:
		apps = json.load(data, object_pairs_hook=OrderedDict)
		print "Loaded: ", filename
		return apps
	print "Failed to load JSON file"
	return null


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
	for current in ids:
		count += 1	
		url ="https://store.steampowered.com/api/appdetails?appids=" + str(current) + "&cc=gb&l=en"
		print count, url
		# Steam API limits may occur (estimated to be around 100 per 5 minutes)
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		#collection.append(data)
		with open('append.json', 'a') as outfile:
			json.dump(data, outfile, indent=4, separators=(',', ':'))
		print "JSON file retrieved from Steam Web API"

	return collection


def write_to_file(collection):
	with open('output.json', 'w') as outfile:
		json.dumps(collection, outfile, sort_keys=True, indent=4)
	print "Data has been written to JSON file"

apps = get_game_ids(get_json_file())
collection = get_steam_api_data(apps)
#write_to_file(collection)

print("Miner Completed")
print "--------------------"

