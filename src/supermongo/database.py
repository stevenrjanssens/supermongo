"""database.py -- tools to interface with MongoDB"""

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def _get_database():
    mongocloud_user = os.getenv('MONGOCLOUD_USER')
    mongocloud_pass = os.getenv('MONGOCLOUD_PASS')
    uri = f"mongodb+srv://{mongocloud_user}:{mongocloud_pass}@cluster0.sfb5zzw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client['dfimages']

headers_collection = _get_database()['headers']
