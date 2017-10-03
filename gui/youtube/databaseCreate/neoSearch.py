from py2neo import Graph,Node, Relationship, watch, cypher
# from neo4j.v1 import GraphDatabase, basic_auth
#import os
# import json
# import pprint , time, re
#search_input=raw_input()
# graph = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "vodka"))
# session=graph.session()
graph = Graph("http://neo4j:sunil@localhost:7474/db/data/")
#global neo_output
neo_output=[]
def search_on_click(videoId):
	del neo_output[:]
	global neo_output
	id=videoId
	run_parameter="match(n:NewVideo)-[r]->(p:NewVideo) where n.id ='"+id+"' return p"
	#print run_parameter
	output=graph.run(run_parameter).data()
	print type(output)
	# neo_output=output
	return output
	# print type(output)
	# for obj in output:
	# 	print (obj)
#search_on_click(123)
current_video_info=[]
def search_current_detail(videoId):
	pass
	del current_video_info[:]
	global current_video_info
	run_parameter="match(n:NewVideo) where n.id ='"+videoId+"' return n"
	#print run_parameter
	current_video_info=graph.run(run_parameter).data()
	return current_video_info
#search_current_detail(search_input)