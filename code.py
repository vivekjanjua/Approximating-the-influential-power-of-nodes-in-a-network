from pymongo import MongoClient
client = MongoClient(“mongodb://localhost:27017/”)

db = client['blogtest']
mycollection = db['users']

f = open("network_graph.txt","a")

for i in db.users.find():
	list = i["friendsList"]
	for j in list:
		//print(j["_id"])
		f.write(str(int(i["_id"]))+" "+str(int(j["_id"]))+"\n")
	
f.close()