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

graph = Graph("http://neo4j:sunil@localhost:7474/db/data/")


for file in os.listdir(os.path.join(os.getcwd(), "test")):
	if file.endswith('.json'):
		data_file = open("test/" + file,'r')
		data = json.load(data_file)
		newVideo = Node("NewVideo")
		newVideo["thumbnail"]=data["videoInfo"]["snippet"]["thumbnails"]["default"]["url"]
		if findkeys(data,"tags") == 1:
			newVideo["tags"] = data["videoInfo"]["snippet"]["tags"]
		else:
			newVideo["tags"] = []
		newVideo["channelId"] = data["videoInfo"]["snippet"]["channelId"]
		newVideo["publishedAt"]=data["videoInfo"]["snippet"]["publishedAt"]
		newVideo["channelTitle"]=data["videoInfo"]["snippet"]["channelTitle"]
		newVideo["title"]=data["videoInfo"]["snippet"]["title"]
		newVideo["categoryId"]=data["videoInfo"]["snippet"]["categoryId"]
		#newVideo["localizedDescription"]=data["videoInfo"]["snippet"]["localized"]["description"]
		#newVideo["localizedTitle"]=data["videoInfo"]["snippet"]["localized"]["title"]
		newVideo["description"] = getTerms(data["videoInfo"]["snippet"]["description"])
		newVideo["commentCount"] = data["videoInfo"]["statistics"]["commentCount"]
		newVideo["viewCount"] = data["videoInfo"]["statistics"]["viewCount"]
		newVideo["favoriteCount"] = data["videoInfo"]["statistics"]["favoriteCount"]
		newVideo["dislikeCount"] = data["videoInfo"]["statistics"]["dislikeCount"]
		newVideo["likeCount"] = int(data["videoInfo"]["statistics"]["likeCount"])
		newVideo["etag"]=data["videoInfo"]["etag"]
		newVideo["id"]=data["videoInfo"]["id"]
		data_file.close()
		graph.create(newVideo)

print("Nodes inserted")

graph.run("Match (n1:NewVideo),(n2:NewVideo) Where  n1 <> n2 AND n1.channelId = n2.channelId  Create (n1)-[r:SAME_CHANNEL]->(n2) return count(r)")

print("1st relation inserted")

graph.run("Match (n1:NewVideo),(n2:NewVideo) Where  n1 <> n2 AND n1.tags is not null AND n2.tags is not null AND size(filter(x in n1.tags where x in n2.tags)) > 0  Create (n1)-[r:commanTag {weight:size(filter(x in n1.tags where x in n2.tags ))}]->(n2) return count(r)")

print("2nd relation inserted")

# Third relation 18min. aprox
graph.run("match (n1:NewVideo),(n2:NewVideo) where n1 <> n2 AND length(filter(x in n1.description where x in n2.description )) > 0  Create (n1)-[r:SIMILAR_DESC {weight:size(filter(x in n1.description where x in n2.description ))}]->(n2) return count(r)")
print("3rd relation inserted")


#Fourth relation
graph.run("match(n1:NewVideo),(n2:NewVideo) where n1<>n2 AND n1.categoryId=n2.categoryId create(n1)-[r:SAME_CATEGORY]->(n2) return count(r) ")
print("4th relation inserted")


#fifth relation
graph.run("Match (n1:NewVideo),(n2:NewVideo) Where  n1 <> n2 AND n1.title is not null AND n2.title is not null AND size(filter(x in n1.title where x in n2.title)) > 0  Create (n1)-[r:commanTitle {weight:size(filter(x in n1.title where x in n2.title ))}]->(n2) return count(r)")
print("5th relation inserted")