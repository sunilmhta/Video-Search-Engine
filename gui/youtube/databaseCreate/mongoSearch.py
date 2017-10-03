from __future__ import print_function
import pymongo
import pprint
from operator import itemgetter
from collections import Counter
conn = pymongo.MongoClient('mongodb://localhost')
import sys
sys.path.insert(0, '/home/sunil/Documents/assignment/gui/youtube/databaseCreate')
import handler

# conn.admin.authenticate('admin','vodka')
db = conn.practice
coll = db.practice_collection
sorted_output=[]
def search(context,username):
	#print context
	del sorted_output[:]
	global sorted_output
	search_input=map(str,context['message'].split())
	# print search_input
	final_output=[]
	for word in search_input:
		result=coll.find({'$or':[{'videoInfo.snippet.tags':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.title':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.channelTitle':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.localized.description':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.localized.title':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.description':{'$regex':word,'$options':'$i'}},
			{'videoInfo.snippet.categoryId':{'$regex':word,'$options':'$i'}}
			]})
		for obj in result:
			if obj not in final_output:
				final_output.append(obj)
	# print final_output
	count=0
	for obj in final_output:
		viewCount=0
		if username!='login':
			video_id=obj['videoInfo']['id']
			viewCount=handler.search_for_logged_in(video_id,username)
		else:
			video_id=obj['videoInfo']['id']
			viewCount=handler.search_for_not_logged_in(video_id)
		# viewCount=obj['videoInfo']['id']
		unparsed_string=''
		count_occurence=0
		if 'tags' in obj['videoInfo']['snippet']:
			for tag in obj['videoInfo']['snippet']['tags']:
				unparsed_string+=tag.lower()
				unparsed_string+=" "
		if 'title' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['title'].lower().strip('\n')
			unparsed_string+=" "
		if 'channelTitle' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['channelTitle'].lower().strip('\n')
			unparsed_string+=" "
		if 'description' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['description'].lower().strip('\n')
			unparsed_string+=" "
		if 'categoryId' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['categoryId'].lower().strip('\n')
			unparsed_string+=" "
		frequency=Counter(unparsed_string.split())
		#print frequency
		for word in search_input:
			count_occurence+=frequency[word.lower()]
		sorted_output.append([[obj],[viewCount]])
	sorted_output = sorted(sorted_output,key=itemgetter(1))
	return sorted_output.reverse()



json_data=[]
def searchIndividual(videoId):
	del json_data[:]
	global json_data
	result=coll.find({'videoInfo.id':videoId})
	return result

def increase_view_count(video_id):
	output=coll.find({'videoInfo.id':video_id})
	for result in output:
		initial_count=result['videoInfo']['statistics']['viewCount']+1
		coll.update({'videoInfo.id':video_id},{'$set':{'videoInfo.statistics.viewCount':initial_count}})
		# print initial_count
		return initial_count
