import pymongo

conn = pymongo.MongoClient()
memap_db = conn['memap']
users_collection = memap_db['users']
notes_collection = memap_db['notes']