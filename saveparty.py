import pymongo
import dns
import os

client = pymongo.MongoClient(os.environ['MONGO_TOKEN'])

database = client['partydb']['partycollection']

def createParty(_id):
	basicData = {
		'id' : _id,
		'rubels' : 100000,
		'name': "teszt",
		'leader' : "állam",
		'isVoted' : 0,
		'desc' : "lol",
		'ide' : "Komcsi",
	}
	try:
		t = database.insert_one(basicData)
	except:
		print("Error attempting to create new user!")

def save(data):
	try:
		t = database.replace_one({'id' : data['id']}, data)
	except:
		print("Error attempting to save data")


def restoreParty(id):
	try:
		data = database.find_one({'id' : id})
		if data:
			return data
		else:
			print("Could not find data")
	except:
		print("Error attempting to restore data")

def checkPartyExist(_id):
	try:
		data = database.find_one({'id' : _id})
		if data:
			return True
		else:
			return False
	except Exception as e:
		print(str(e))


def parties():
	try:
		data = database.find()
		dataList = sorted(data, key = lambda i: i['rubels'],reverse=True)
		results = dataList[:5]
		return results
	except:
		print("Error trying to get leaderboard data")