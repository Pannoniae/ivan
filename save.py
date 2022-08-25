import pymongo
import dns
import os

client = pymongo.MongoClient(os.environ['MONGO_TOKEN'])

database = client['coinsdb']['coinscollection']

def createUser(_id):
	basicData = {
		'userid' : _id,
		'smackers' : 0,
		'lastTime' : 0,
		'bonusTime' : 0,
	}
	try:
		t = database.insert_one(basicData)
	except:
		print("Error attempting to create new user!")

def save(data):
	try:
		t = database.replace_one({'userid' : data['userid']}, data)
	except:
		print("Error attempting to save data")


def restore(id):
	try:
		data = database.find_one({'userid' : id})
		if data:
			return data
		else:
			print("Could not find data")
	except:
		print("Error attempting to restore data")

def checkExist(_id):
	try:
		data = database.find_one({'userid' : _id})
		if data:
			return True
		else:
			return False
	except Exception as e:
		print(str(e))


def leaderboard():
	try:
		data = database.find()
		dataList = sorted(data, key = lambda i: i['smackers'],reverse=True)
		results = dataList[:5]
		return results
	except:
		print("Error trying to get leaderboard data")

