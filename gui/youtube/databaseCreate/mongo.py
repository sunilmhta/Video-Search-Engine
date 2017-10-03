import os
import pymongo
import json
import pprint

conn = pymongo.MongoClient('mongodb://localhost')
# conn.admin.authenticate('admin','vodka')

db = conn.practice
coll = db.practice_collection
coll.remove()
coll=db.practice_collection
file_names=[]
for file in os.listdir('test'):
    file_names.append(file)
for val in file_names:
    name='test/'+str(val)
    page = open(name,'r')
    parsed = json.loads(page.read())
    coll.insert_many([parsed])