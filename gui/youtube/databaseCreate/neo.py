from py2neo import Graph,Node, Relationship, watch, cypher
import os
import json
import pprint , time, re
#rm -rf data/graph.db
time1 = time.time()


def findkeys(node, kv):
	if isinstance(node, list):
		for i in node:
			if findkeys(i, kv) == 1:
				return 1
	elif isinstance(node, dict):
		if kv in node:
			return 1
		for j in node.values():
			if findkeys(j, kv) == 1:
				return 1



def getTerms(description):
	#replaced = re.sub(r'[^a-zA-Z0-9]+'," ",description)
	#return description.split(" ")
	return re.findall(r'\w+',description)

graph = Graph("http://neo4j:vodka@localhost:7474/db/data/")


for file in os.listdir(os.path.join(os.getcwd(), "test")):
	if file.endswith('.json'):
		data_file = open("test/" + file,'r')
		data = json.load(data_file)
		newVideo = Node("NewVideo")
		newVideo["commentCount"] = data["videoInfo"]["statistics"]["commentCount"]
		newVideo["viewCount"] = data["videoInfo"]["statistics"]["viewCount"]
		newVideo["favoriteCount"] = data["videoInfo"]["statistics"]["favoriteCount"]
		newVideo["dislikeCount"] = data["videoInfo"]["statistics"]["dislikeCount"]
		newVideo["likeCount"] = int(data["videoInfo"]["statistics"]["likeCount"])

		if findkeys(data,"tags") == 1:
			newVideo["tags"] = data["videoInfo"]["snippet"]["tags"]
		else:
			newVideo["tags"] = []
		newVideo["channelId"] = data["videoInfo"]["snippet"]["channelId"]
		newVideo["description"] = getTerms(data["videoInfo"]["snippet"]["description"])

		data_file.close()
		graph.create(newVideo)

print("Nodes inserted")

graph.run("Match (n1:NewVideo),(n2:NewVideo) Where  n1 <> n2 AND n1.channelId = n2.channelId  Create (n1)-[r:hasSameChannelAs]->(n2) return count(r)")

print("1st relation inserted")

graph.run("Match (n1:NewVideo),(n2:NewVideo) Where  n1 <> n2 AND n1.tags is not null AND n2.tags is not null AND length(filter(x in n1.tags where x in n2.tags)) > 0  Create (n1)-[r:hasCommonTagsWith {weight:size(filter(x in n1.tags where x in n2.tags ))}]->(n2) return count(r)")

print("2nd relation inserted")

# Third relation 18min. aprox
graph.run("match (n1:NewVideo),(n2:NewVideo) where n1 <> n2 AND length(filter(x in n1.description where x in n2.description )) > 0  Create (n1)-[r:hasCommonTermsWith {weight:size(filter(x in n1.description where x in n2.description ))}]->(n2) return count(r)")
print("3rd relation inserted")
'''

#match (n1:NewVideo),(n2:NewVideo) where n1 <> n2 AND length(filter(x in n1.description where x in n2.description )) > 0  Create (n1)-[r:hasCommonTermsWith {weight:size(filter(x in n1.description where x in n2.description ))}]->(n2) return count(r)
time2 = time.time()
print(time2 - time1)
'''