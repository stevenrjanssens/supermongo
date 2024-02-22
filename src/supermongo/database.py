"""database.py -- tools to interface with MongoDB"""

from pymongo import MongoClient

def _get_database():
    client = MongoClient("localhost", 27017)
    return client['dfimages']

headers_collection = _get_database()['headers']
